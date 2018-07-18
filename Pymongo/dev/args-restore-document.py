#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint, argparse, string, os
import mylib



"""" Initial args parser """
parser = argparse.ArgumentParser()
parser.add_argument("BACKUP_PATTERN", help="Enter backed up collection's name to restore here.", type=str)
parser.add_argument("BEGIN_DAY", help="Enter start day to search and restore docs here.", type=int)
parser.add_argument("BEGIN_MONTH", help="Enter start month to search and restore docs here.", type=int)
parser.add_argument("BEGIN_YEAR", help="Enter start year to search and restore docs here.", type=int)
parser.add_argument("END_DAY", help="Enter end day to search and restore docs here.", type=int)
parser.add_argument("END_MONTH", help="Enter end month to search and restore docs here.", type=int)
parser.add_argument("END_YEAR", help="Enter end year to search and restore docs here.", type=int)
parser.add_argument("DIR", help="Enter full path to dumped BSON files here.", type=str)
args = parser.parse_args()


""" Clean up and standallize input args """
PATTERN_PUNCTUATION = """!"#$%&'()*+,./:;<=>?@[\]^`{|}~"""
OSPATH_PUNCTUATION = """!"#$%&'()*+,:;<=>?@[\]^`{|}~"""
BACKUP_PATTERN = args.BACKUP_PATTERN.translate(None, PATTERN_PUNCTUATION)
DIR = os.path.normpath(args.DIR.translate(None, OSPATH_PUNCTUATION)) + '/'
print("BACKUP_PATTERN: ", BACKUP_PATTERN)
print("DIR: ", DIR)


""" Check if DIR is existed. If not, exit with error."""
if os.path.isdir(DIR) == False:
    print(DIR, "is not existed. Exit now.")
    exit(1)
else:
    print(DIR, "is existed. Process to next step.")


"""MongoDB connection"""
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['mondra_log_restore']
collection = db[BACKUP_PATTERN]

""" Time range to restore."""
BEGIN_DAY = 2
BEGIN_MONTH = 12
BEGIN_YEAR = 2016
END_DAY = 3
END_MONTH = 12
END_YEAR = 2016
BEGIN_PART_NUM = 1


""" Droping existing collection """
### Script is not designed to handle duplicate documents. 
### In case of having duplicated documents, consider either importing to another collection or drop existing collection.
### Here, I commented out the drop command to stay on the safe side  :)
### collection.drop()


"""Validate time range"""
VALIDATOR = mylib.timerange_validate(BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, END_DAY, END_MONTH, END_YEAR)
if VALIDATOR == 1:
    exit(1)


for YEAR in range(BEGIN_YEAR, END_YEAR+1):
    if YEAR != END_YEAR:
        for MONTH in range(1, 13):
            if MONTH == 2:
                if YEAR % 400 == 0 or (YEAR % 4 == 0 and YEAR % 100 != 0):
                    for DAY in range(1, 30):
                        mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                else:
                    for DAY in range(1, 29):
                        mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            elif MONTH == 4 or MONTH == 6 or MONTH == 9 or MONTH == 11:
                for DAY in range(1, 31):
                    mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for DAY in range(1, 32):
                    mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
    else:
        for MONTH in range(BEGIN_MONTH, END_MONTH+1):
            if MONTH != END_MONTH:
                if MONTH == 2:
                    if YEAR % 400 == 0 or (YEAR % 4 == 0 and YEAR % 100 != 0):
                        for DAY in range(1, 30):
                            mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                    else:
                        for DAY in range(1, 29):
                            mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                elif MONTH == 4 or MONTH == 6 or MONTH == 9 or MONTH == 11:
                    for DAY in range(1, 31):
                        mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                else:
                    for DAY in range(1, 32):
                        mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for DAY in range(BEGIN_DAY, END_DAY+1):
                    mylib.restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)



#### This part is used to test result after import
# """Generate cursor to find document"""
# cursor = collection.find().max_scan(1000)
# total = 0
# for docs in cursor:
#     pprint.pprint(docs)
#     total +=1
# print ("total ",total," docs")
######################################################