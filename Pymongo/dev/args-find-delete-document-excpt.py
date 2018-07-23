#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import mylib
import time, datetime, calendar, argparse, string, os



"""" Initial args parser """
parser = argparse.ArgumentParser()
parser.add_argument("BACKUP_PATTERN", help="Enter collection's name here.", type=str)
parser.add_argument("INDEX_PATTERN", help="Enter indexed field here.", type=str)
args = parser.parse_args()


""" Clean up and standallize input args """
PATTERN_PUNCTUATION = """!"#$%&'()*+,./:;<=>?@[\]^`{|}~"""
BACKUP_PATTERN = args.BACKUP_PATTERN.translate(None, PATTERN_PUNCTUATION)
INDEX_PATTERN = args.INDEX_PATTERN.translate(None, PATTERN_PUNCTUATION)
print("BACKUP_PATTERN: ", BACKUP_PATTERN)
print("INDEX_PATTERN: ", INDEX_PATTERN)


"""MongoDB connection"""
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['mondra_log']
collection = db[BACKUP_PATTERN]


""" Time range to backup
    END_DATE_RAW is calculated by:  (1) from today, go to the last day of previous month
                                    (2) from (1), go backward 100 days (more than 3 months), then
    END_MONTH, END_YEAR are extracted from END_DATE_RAW, and
    END_DAY is the last day of END_MONTH.

    BEGIN_PART_NUM
    If 1 day contains more than 50.000 record, data is split to parts, starting from BEGIN_PART_NUM (data_1, data_2, data_3...)
    In case of recovering from interuptted run, move existing data to another directory before executing the script.
"""
BEGIN_DAY = 1
BEGIN_MONTH = 12
BEGIN_YEAR = 2015
BEGIN_PART_NUM = 1
END_DATE_RAW = datetime.date.today() + datetime.timedelta(days=-int(datetime.date.today().strftime("%e"))) + datetime.timedelta(days=-100)
END_MONTH = int(END_DATE_RAW.strftime("%m"))
END_YEAR = int(END_DATE_RAW.strftime("%G"))
END_DAY = calendar.monthrange(END_YEAR,END_MONTH)[1]


"""Validate time range"""
VALIDATOR = mylib.timerange_validate(BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, END_DAY, END_MONTH, END_YEAR)
if VALIDATOR == 1:
    exit(1)


"""
    Main task.
    Loop through each day: query block of 50.000 records, write to file, delete.
"""
for YEAR in range(BEGIN_YEAR, END_YEAR+1):
    if YEAR != END_YEAR:
        for MONTH in range(1, 13):
            if MONTH == 2:
                if YEAR % 400 == 0 or (YEAR % 4 == 0 and YEAR % 100 != 0):
                    for DAY in range(1, 30):
                        mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                else:
                    for DAY in range(1, 29):
                        mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            elif MONTH == 4 or MONTH == 6 or MONTH == 9 or MONTH == 11:
                for DAY in range(1, 31):
                    mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for DAY in range(1, 32):
                    mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
    else:
        for MONTH in range(BEGIN_MONTH, END_MONTH+1):
            if MONTH != END_MONTH:
                if MONTH == 2:
                    if YEAR % 400 == 0 or (YEAR % 4 == 0 and YEAR % 100 != 0):
                        for DAY in range(1, 30):
                            mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                    else:
                        for DAY in range(1, 29):
                            mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                elif MONTH == 4 or MONTH == 6 or MONTH == 9 or MONTH == 11:
                    for DAY in range(1, 31):
                        mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                else:
                    for DAY in range(1, 32):
                        mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for DAY in range(BEGIN_DAY, END_DAY+1):
                    mylib.excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            
"""Delete all empty dumped files and move data files to directory"""
mylib.re_arrange(BACKUP_PATTERN)



#pprint.pprint (db.current_op())
#pprint.pprint(collection.find_one())


"""Main archive engine, find, backup and delete document"""
def excpt_backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM):
    
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
        totaldel = 0
        with open(DELETELIST_FILENAME, 'wb') as lf:
            with open(OUTPUT_FILENAME, 'wb') as tf:
                for item in cursor:
                    total += 1
                    eitem = 'ObjectId' + '(\"' + str(item['_id']) + '\")'
                    # print ("Add docs to delete: "+ str(eitem))
                    tf.write(BSON.encode(item))
                    lf.write(str(eitem)+'\n')
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
                    if int(RESULT.deleted_count) > 0:
                        totaldel += 1
                    # print ("Deleting: ",ID,"   Return: ",RESULT.deleted_count)
                    # time.sleep(0.001)
            PART_NUM += 1
        print(DELETELIST_FILENAME+"Total deleted documents: ", totaldel)

        print ("Current FLAG: ",FLAG)
        print ("Last filename: ",DELETELIST_FILENAME)
        print;print;print;
"""*******************End of def**************************************"""