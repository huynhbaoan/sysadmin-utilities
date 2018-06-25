#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint
import mylib


"""MongoDB connection"""
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['mondra_log_restore']
collection = db['GameRewardLog']
BACKUP_PATTERN = 'GameRewardLog'
DIR = '/home/huynhbaoan/PythonProject/Pymongo/dev/'

collection.drop()
# print(collection)

""" Time range to backup
    Be careful with BEGIN_PART_NUM."""
BEGIN_MONTH = 1
BEGIN_YEAR = 2016
END_MONTH = 2
END_YEAR = 2016
BEGIN_PART_NUM = 1


"""Validate time range"""
VALIDATOR = mylib.timerange_validate(BEGIN_MONTH, BEGIN_YEAR, END_MONTH, END_YEAR)
if VALIDATOR == 1:
    exit(1)


"""Main restore task"""
for YEAR in range(BEGIN_YEAR, END_YEAR+1):
    if BEGIN_YEAR == END_YEAR:
        for MONTH in range(BEGIN_MONTH, END_MONTH+1):
            mylib.restore_docs(DIR, BACKUP_PATTERN, MONTH, YEAR, collection, BEGIN_PART_NUM)
        break
    else:
        if YEAR == BEGIN_YEAR:
            for MONTH in range(BEGIN_MONTH, 13):
                mylib.restore_docs(DIR, BACKUP_PATTERN, MONTH, YEAR, collection, BEGIN_PART_NUM)
        else:
            if YEAR != END_YEAR:
                for MONTH in range(1, 13):
                    mylib.restore_docs(DIR, BACKUP_PATTERN, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for MONTH in range(1, END_MONTH+1):
                    mylib.restore_docs(DIR, BACKUP_PATTERN, MONTH, YEAR, collection, BEGIN_PART_NUM)


# """Generate cursor to find document"""
# cursor = collection.find().max_scan(100000)
# total = 0
# for docs in cursor:
#     pprint.pprint(docs)
#     total +=1
# print ("total ",total," docs")