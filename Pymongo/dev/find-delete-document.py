#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import mylib



"""MongoDB connection"""
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['mondra_log']
collection = db['GameRewardLog']
BACKUP_PATTERN = 'GameRewardLog'
# collection = db['BattleReport_01_01_2017']


""" Time range to backup
    Be careful with BEGIN_PART_NUM."""
BEGIN_MONTH = 12
BEGIN_YEAR = 2015
END_MONTH = 12
END_YEAR = 2016
BEGIN_PART_NUM = 2


"""Validate time range"""
VALIDATOR = mylib.timerange_validate(BEGIN_MONTH, BEGIN_YEAR, END_MONTH, END_YEAR)
if VALIDATOR == 1:
    exit(1)


"""Main backup task"""
for YEAR in range(BEGIN_YEAR, END_YEAR+1):
    if BEGIN_YEAR == END_YEAR:
        for MONTH in range(BEGIN_MONTH, END_MONTH+1):
            mylib.backup_delete_docs(BACKUP_PATTERN, BEGIN_MONTH, BEGIN_YEAR, MONTH, YEAR, collection, BEGIN_PART_NUM)
        break
    else:
        if YEAR == BEGIN_YEAR:
            for MONTH in range(BEGIN_MONTH, 13):
                mylib.backup_delete_docs(BACKUP_PATTERN, BEGIN_MONTH, BEGIN_YEAR, MONTH, YEAR, collection, BEGIN_PART_NUM)
        else:
            if YEAR != END_YEAR:
                for MONTH in range(1, 13):
                    mylib.backup_delete_docs(BACKUP_PATTERN, BEGIN_MONTH, BEGIN_YEAR, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for MONTH in range(1, END_MONTH+1):
                    mylib.backup_delete_docs(BACKUP_PATTERN, BEGIN_MONTH, BEGIN_YEAR, MONTH, YEAR, collection, BEGIN_PART_NUM)

mylib.re_arrange('GameRewardLog')



#pprint.pprint (db.current_op())
#pprint.pprint(collection.find_one())