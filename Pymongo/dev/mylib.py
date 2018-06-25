#!/usr/bin/python

from bson import BSON, Binary, Code, decode_all
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
from pymongo import InsertOne, DeleteOne, ReplaceOne
import pprint, datetime, time, os, errno, glob, shutil



"""Time range validator"""
def timerange_validate (BEGIN_MONTH, BEGIN_YEAR, END_MONTH, END_YEAR):
    """Validate time range to cut log"""
    if BEGIN_YEAR > END_YEAR:
        print ("Invalid time range. END YEAR is lower than BEGIN YEAR")
        RESULT = 1
    elif BEGIN_YEAR == END_YEAR:
        if BEGIN_MONTH > END_MONTH:
            print ("Invalid time range. END MONTH is lower than BEGIN MONTH")
            RESULT = 1
        else:
            RESULT = 0
    else:
        RESULT = 0
    return RESULT
"""*******************End of def*****************************************"""


"""Main archive engine, find, backup and delete document"""
def backup_delete_docs(BACKUP_PATTERN, BEGIN_MONTH, BEGIN_YEAR, MONTH, YEAR, collection, BEGIN_PART_NUM):
    
    """Convert normal DATE to EPOCH DATE"""
    BEGIN_DATE = datetime.datetime(BEGIN_YEAR,BEGIN_MONTH,1,0,0,0)
    END_DATE = datetime.datetime(YEAR,MONTH,1,0,0,0)
    EPOCH = datetime.datetime.utcfromtimestamp(0)
    E_BEGIN_DATE = (BEGIN_DATE - EPOCH).total_seconds() * 1000
    E_END_DATE = (END_DATE - EPOCH).total_seconds() * 1000




    FLAG = 0
    PART_NUM = BEGIN_PART_NUM
    while FLAG == 0:
        """Generate cursor to find document"""
        print("Searching 50.000 docs to delete...")
        cursor = collection.find( { '$and': [
            {'createdAt': { '$lt': E_END_DATE } }, \
            {'createdAt': { '$gte': E_BEGIN_DATE } } \
            ] } )\
            .max_scan(50000)
        # pprint.pprint(cursor.explain())

        """Sleep to reduce memory stress on Mongo server"""
        print ("Waiting 10 sencond for Mongo server...")
        time.sleep(10)

        """Generate filename to backup/delete"""    
        OUTPUT_FILENAME = str(BACKUP_PATTERN)+'_xx_'+str(MONTH)+'_'+str(YEAR)+'_'+str(PART_NUM)+'.bson'
        DELETELIST_FILENAME = str(BACKUP_PATTERN)+'_xx_'+str(MONTH)+'_'+str(YEAR)+'_'+str(PART_NUM)+'.txt'

        """Backup, list docs to delete"""
        total = 0
        with open(DELETELIST_FILENAME, 'wb') as lf:
            with open(OUTPUT_FILENAME, 'wb') as tf:
                for item in cursor:
                    total += 1
                    print ("Add docs to delete: "+item['_id'])
                    tf.write(BSON.encode(item))
                    lf.write(str(item['_id'])+'\n')
        print (OUTPUT_FILENAME+" total documents: ", total)
        time.sleep(2)

        
        """Decide either stop or continue to search"""
        if (os.stat(DELETELIST_FILENAME).st_size == 0) == True:
            FLAG = 1
            print (DELETELIST_FILENAME+": No more docs to delete")
        else:
            FLAG = 0

            """Else, Delete docs"""
            print (DELETELIST_FILENAME+": BEGIN DELETING DOCS!")
            with open(DELETELIST_FILENAME, 'rb') as lf:
                for line in lf:
                    ID = line.rstrip()
                    RESULT = collection.delete_one({'_id': ID})
                    print ("Deleting: ",ID,"   Return: ",RESULT.deleted_count)
                    time.sleep(0.001)

            PART_NUM += 1

        print ("Current FLAG: ",FLAG)
        print ("Last filename: ",DELETELIST_FILENAME)



"""*******************End of def**************************************"""



"""Move backed up file to new location"""
def re_arrange(BACKUP_PATTERN):
    
    """Rename any exitsted files/directories to avoid overwriting data"""
    TEMPSRC = BACKUP_PATTERN
    if os.path.exists(TEMPSRC) == True:
        TEMPDST = BACKUP_PATTERN+'_old'
        print("Move ",TEMPSRC," to ",TEMPDST)
        os.rename(TEMPSRC, TEMPDST)
    
    TEMPSRC = BACKUP_PATTERN+'_removelist'
    if os.path.exists(TEMPSRC) == True:
        TEMPDST = BACKUP_PATTERN+'_removelist_old'
        print("Move ",TEMPSRC," to ",TEMPDST)
        os.rename(TEMPSRC, TEMPDST)

    """Create directory"""
    try:
        os.makedirs(BACKUP_PATTERN+'_removelist',mode=0o755)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise SystemExit
    try:
        os.makedirs(BACKUP_PATTERN,mode=0o755)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise SystemExit
            
    print("Begin cleaning up files.")
    """Remove empty file, then 
    Move all .bson, .txt file to new directory"""
    for file in glob.glob(BACKUP_PATTERN+"*.bson"):
        if (os.stat(file).st_size == 0) == True:
            print("Delete ",file)
            os.remove(file)
        else:
            print("Move ",file)
            shutil.move(file, BACKUP_PATTERN)
    DST = BACKUP_PATTERN+'_removelist'
    for file in glob.glob(BACKUP_PATTERN+"*.txt"):
        if (os.stat(file).st_size == 0) == True:
            print("Delete ",file)
            os.remove(file)
        else:
            print("Move ",file)
            shutil.move(file, DST)
"""*******************End of def**************************************"""



""" Main engine to restore docs from bson """
def restore_docs(DIR, BACKUP_PATTERN, MONTH, YEAR, collection, BEGIN_PART_NUM):
    
    # FULLPATH = os.path.join(DIR + BACKUP_PATTERN, BACKUP_PATTERN + "_xx_" + str(MONTH) + \
    #             "_" + str(YEAR))
    FULLPATH = os.path.join(DIR + BACKUP_PATTERN + "_old", BACKUP_PATTERN + "_xx_" + str(MONTH) + \
            "_" + str(YEAR))
    for file in glob.glob(FULLPATH + "*.bson"):
        print ("Restoring from ",file)    
        with open(file, 'rb') as f:
            collection.insert(decode_all(f.read()))
