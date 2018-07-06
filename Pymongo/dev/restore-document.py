#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint
import mylib


BACKUP_PATTERN = 'GameRewardLog'


"""MongoDB connection"""
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['mondra_log_restore']
collection = db[BACKUP_PATTERN]

DIR = '/home/huynhbaoan/PythonProject/Pymongo/dev/'


""" Time range to backup
    Be careful with BEGIN_PART_NUM."""
BEGIN_DAY = 2
BEGIN_MONTH = 12
BEGIN_YEAR = 2016
END_DAY = 3
END_MONTH = 12
END_YEAR = 2016
BEGIN_PART_NUM = 1


#collection.drop()


"""Validate time range"""
VALIDATOR = mylib.timerange_validate(BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, END_DAY, END_MONTH, END_YEAR)
if VALIDATOR == 1:
    exit(1)


for YEAR in range(BEGIN_YEAR, END_YEAR+1):
    if YEAR != END_YEAR:
        for MONTH in range(1, 13):
            if MONTH == 2:
                if YEAR % 4 == 0:
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
                    if YEAR % 4 == 0:
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
# cursor = collection.find().max_scan(100000)
# total = 0
# for docs in cursor:
#     pprint.pprint(docs)
#     total +=1
# print ("total ",total," docs")
######################################################