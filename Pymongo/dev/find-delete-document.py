#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import mylib
import time, datetime, calendar


BACKUP_PATTERN = 'GameRewardLog'
INDEX_PATTERN = 'createdAt'


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
                        mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                else:
                    for DAY in range(1, 29):
                        mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            elif MONTH == 4 or MONTH == 6 or MONTH == 9 or MONTH == 11:
                for DAY in range(1, 31):
                    mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for DAY in range(1, 32):
                    mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
    else:
        for MONTH in range(BEGIN_MONTH, END_MONTH+1):
            if MONTH != END_MONTH:
                if MONTH == 2:
                    if YEAR % 400 == 0 or (YEAR % 4 == 0 and YEAR % 100 != 0):
                        for DAY in range(1, 30):
                            mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                    else:
                        for DAY in range(1, 29):
                            mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                elif MONTH == 4 or MONTH == 6 or MONTH == 9 or MONTH == 11:
                    for DAY in range(1, 31):
                        mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
                else:
                    for DAY in range(1, 32):
                        mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            else:
                for DAY in range(BEGIN_DAY, END_DAY+1):
                    mylib.backup_delete_docs(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
            
"""Delete all empty dumped files and move data files to directory"""
mylib.re_arrange(BACKUP_PATTERN)



#pprint.pprint (db.current_op())
#pprint.pprint(collection.find_one())