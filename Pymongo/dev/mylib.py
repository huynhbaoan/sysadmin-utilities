#!/usr/bin/python

from bson import BSON, Binary, Code, decode_all
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
from pymongo import InsertOne, DeleteOne, ReplaceOne
import pprint, datetime, time, calendar, sys, os, errno, glob, shutil
import tarfile, gzip



"""Time range validator"""
def timerange_validate (BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, END_DAY, END_MONTH, END_YEAR):
    """Validate time range to cut log"""
    RESULT = 2
    if BEGIN_YEAR > END_YEAR:
        print ("Invalid time range. END YEAR is lower than BEGIN YEAR")
        RESULT = 1
    elif BEGIN_YEAR == END_YEAR:
        if BEGIN_MONTH > END_MONTH:
            print ("Invalid time range. END MONTH is lower than BEGIN MONTH")
            RESULT = 1
        elif BEGIN_MONTH == END_MONTH:
            if BEGIN_DAY > END_DAY:
                print ("Invalid time range. END DAY is lower than BEGIN DAY")
                RESULT = 1
            else:
                RESULT = 0
    else:
        RESULT = 0
    return RESULT
"""*******************End of def*****************************************"""



"""Main archive engine, find, backup and delete document"""
def backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM):
    
    """Convert normal DATE to EPOCH DATE"""
    BEGIN_DATE = datetime.datetime(BEGIN_YEAR,BEGIN_MONTH,BEGIN_DAY,0,0,0)
    END_DATE = datetime.datetime(YEAR,MONTH,DAY,0,0,0)
    EPOCH = datetime.datetime.utcfromtimestamp(0)
    E_BEGIN_DATE = (BEGIN_DATE - EPOCH).total_seconds() * 1000
    E_END_DATE = (END_DATE - EPOCH).total_seconds() * 1000


    FLAG = 0
    PART_NUM = BEGIN_PART_NUM
    while FLAG == 0:

        """Generate filename to backup/delete"""    
        OUTPUT_FILENAME = str(BACKUP_PATTERN)+'_'+str(DAY)+'_'+str(MONTH)+'_'+str(YEAR)+'_'+str(PART_NUM)+'.bson'
        DELETELIST_FILENAME = str(BACKUP_PATTERN)+'_'+str(DAY)+'_'+str(MONTH)+'_'+str(YEAR)+'_'+str(PART_NUM)+'.txt'
        print ("Current filename: ",DELETELIST_FILENAME)

        """Generate cursor to find document"""
        print ("Searching 50.000 docs to delete...")
        cursor = collection.find( { '$and': [
            {INDEX_PATTERN: { '$lt': E_END_DATE } }, \
            {INDEX_PATTERN: { '$gte': E_BEGIN_DATE } } \
            ] } )\
            .max_scan(50000)
        # pprint.pprint(cursor.explain())    # leave here to debug of neccessary


        """Backup, list docs to delete"""
        total = 0
        with open(DELETELIST_FILENAME, 'wb') as lf:
            with open(OUTPUT_FILENAME, 'wb') as tf:
                for item in cursor:
                    total += 1
                    print ("Add docs to delete: "+item['_id'])
                    tf.write(BSON.encode(item))
                    lf.write(str(item['_id'])+'\n')
        print (OUTPUT_FILENAME+" .Total documents: ", total)

        if total > 0:
            """Sleep to reduce memory stress on Mongo server"""
            print ("Search completed. Waiting 2 seconds for Mongo server...")
            time.sleep(2)
        else:
            print ("No docs found. Skip waiting.")

        
        """Decide either stop or continue to search"""
        """FLAG 0: continue, FLAG 1: stop"""
        """DELETELIST_FILENAME = 0 bytes mean no record to delete, then stop"""
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
                    #time.sleep(0.001)

            PART_NUM += 1

        print ("Current FLAG: ",FLAG)
        print ("Last filename: ",DELETELIST_FILENAME)
        print;print;print;
"""*******************End of def**************************************"""



"""Move backed up file to new location"""
def re_arrange(BACKUP_PATTERN):
    
    """Rename any exitsted files/directories based on current timestamp to avoid overwriting data"""
    CURRENT_DATE = str(datetime.date.today()).replace("-","")
    CURRENT_TIME = str(datetime.datetime.now().time()).replace(":","").split(".")[0]
    TEMPSRC = BACKUP_PATTERN
    if os.path.exists(TEMPSRC) == True:
        TEMPDST = BACKUP_PATTERN+'_'+CURRENT_DATE+'_'+CURRENT_TIME
        print("Move ",TEMPSRC," to ",TEMPDST)
        os.rename(TEMPSRC, TEMPDST)
    
    TEMPSRC = BACKUP_PATTERN+'_removelist'
    if os.path.exists(TEMPSRC) == True:
        TEMPDST = BACKUP_PATTERN+'_removelist_'+CURRENT_DATE+'_'+CURRENT_TIME
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
            print("Delete empty BSON file ",file)
            os.remove(file)
        else:
            print("Move ",file)
            shutil.move(file, BACKUP_PATTERN)
    DST = BACKUP_PATTERN+'_removelist'
    for file in glob.glob(BACKUP_PATTERN+"*.txt"):
        if (os.stat(file).st_size == 0) == True:
            print("Delete empty LIST ",file)
            os.remove(file)
        else:
            print("Move ",file)
            shutil.move(file, DST)
"""*******************End of def**************************************"""



""" Restore docs from BSON file """
def restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM):
    
    FULLPATH = os.path.join(DIR + BACKUP_PATTERN, BACKUP_PATTERN + "_" + str(DAY) + \
                "_" + str(MONTH) + "_" + str(YEAR))
    print ("Restoring ",BACKUP_PATTERN,DAY,MONTH,YEAR)
    for file in glob.glob(FULLPATH + "*.bson"):
        print ("Restoring from ",file)    
        with open(file, 'rb') as f:
            collection.insert(decode_all(f.read()))
"""*******************End of def**************************************"""



""" Compress BSON file  """
def compress_docs(DIR, BACKUP_PATTERN, MONTH, YEAR):
    LISTDIR = []

    ### Get list of child directories inside backed up directory.
    ### Break: only decend 1 level 
    for (root, dirs, files) in os.walk(DIR, topdown=True, followlinks=False):
        LISTDIR = dirs
        break

    ### Filter child directories list. Only scan .BSON file inside directories which have BACKUP_PATTERN
    for CHILD_DIR in LISTDIR:
        if BACKUP_PATTERN in CHILD_DIR and '_removelist' not in CHILD_DIR:
            ### Get FULLPATH, use for glob scan later
            FULLPATH = os.path.join(DIR , CHILD_DIR)

            ### Create archive
            TARFILE = os.path.join(DIR, CHILD_DIR, BACKUP_PATTERN + '_' + str(MONTH) + '_' + str(YEAR) + '.tar.gz')
            if os.path.isfile(TARFILE) != True:
                try:
                    with tarfile.TarFile.gzopen(TARFILE, mode='w', compresslevel=9) as targz:
                        print("Create archive: ", TARFILE)
                        for FILE in glob.glob(FULLPATH + '/' + BACKUP_PATTERN + '_*_' + str(MONTH) + '_' + str(YEAR) + '_*' + ".bson"):
                            try:
                                ### Split head, tail to avoid adding fullpath to tarfile
                                head, tail = os.path.split(FILE)
                                targz.add(FILE, arcname=tail)
                                print("Compressed BSON file: ", tail)
                            except:
                                print("Error adding file ", FILE, "Error: ", sys.exc_info())
                                raise
                except:
                    print("Unexpected error:", sys.exc_info())
                    raise

                ### Delete compressed .BSON files
                for FILE in glob.glob(FULLPATH + '/' + BACKUP_PATTERN + '_*_' + str(MONTH) + '_' + str(YEAR) + '_*' + ".bson"):
                    print("Delete compressed BSON file: ", FILE)
                    os.remove(FILE)

            else:
                print("File existed, cannot create new archive: ",TARFILE)

            if (os.stat(TARFILE).st_size < 100) == True:
                print("Delete empty archive file ",TARFILE)
                os.remove(TARFILE)

            ### Uncomment this block to check content inside tar file
            # print
            # print('Contents:')
            # t = tarfile.open(TARFILE, 'r')
            # for member_info in t.getmembers():
            #     print(member_info.name)
            # print
            ###########################################################

        ### Remove all contents inside BACKUP_PATTERN_removelist directory
        ### NOTE: NEVER put any data files inside this directory. 
        ### Files inside this directory is temporary file, and are used to store temporary pointer's address only
        if BACKUP_PATTERN in CHILD_DIR and '_removelist' in CHILD_DIR:
            FULLPATH = os.path.join(DIR , CHILD_DIR)
            shutil.rmtree(FULLPATH)
"""*******************End of def**************************************"""