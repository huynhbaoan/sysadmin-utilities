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


""" Try to resume from last run. """
BEGIN_DATE_RAW = mylib.resume_stdid(BACKUP_PATTERN, INDEX_PATTERN, collection)


""" Time range to backup
    END_DATE_RAW is calculated by:  (1) from today, go to the last day of previous month
                                    (2) from (1), go backward 100 days (more than 3 months), then
    END_MONTH, END_YEAR are extracted from END_DATE_RAW, and
    END_DAY is the last day of END_MONTH.

    BEGIN_PART_NUM
    If 1 day contains more than 50.000 record, data is split to parts, starting from BEGIN_PART_NUM (data_1, data_2, data_3...)
    In case of recovering from interuptted run, move existing data to another directory before executing the script.
"""
BEGIN_DAY = int(BEGIN_DATE_RAW.strftime("%d"))
BEGIN_MONTH = int(BEGIN_DATE_RAW.strftime("%m"))
BEGIN_YEAR = int(BEGIN_DATE_RAW.strftime("%G"))
BEGIN_PART_NUM = 1


END_DATE_RAW = datetime.date.today() + datetime.timedelta(days=-int(datetime.date.today().strftime("%e"))) + datetime.timedelta(days=-100)
END_MONTH = int(END_DATE_RAW.strftime("%m"))
END_YEAR = int(END_DATE_RAW.strftime("%G"))
END_DAY = calendar.monthrange(END_YEAR,END_MONTH)[1]
END_DATE_STR = str(END_DAY) + ' ' + str(END_MONTH) + ' ' + str(END_YEAR)
END_DATE_RAW = datetime.datetime.strptime(END_DATE_STR, '%d %m %Y')


print("CONTINUE FROM... ", BEGIN_DATE_RAW, "TO... ", END_DATE_RAW)
time.sleep(5)

"""Validate time range"""
VALIDATOR = mylib.timerange_validate(BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, END_DAY, END_MONTH, END_YEAR)
if VALIDATOR == 1:
    exit(1)


"""
    Main task.
    Loop through each day: query block of 50.000 records, write to file, delete.
"""
DATE_RAW = BEGIN_DATE_RAW
while (DATE_RAW <= END_DATE_RAW): 
    DAY = int(DATE_RAW.strftime("%d"))
    MONTH = int(DATE_RAW.strftime("%m"))
    YEAR = int(DATE_RAW.strftime("%G"))
    mylib.backup_delete_docs_stdid(BACKUP_PATTERN, INDEX_PATTERN, BEGIN_DAY, BEGIN_MONTH, BEGIN_YEAR, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM)
    DATE_RAW = DATE_RAW+ datetime.timedelta(days=1)


"""Delete all empty dumped files and move data files to directory"""
mylib.re_arrange(BACKUP_PATTERN)


#pprint.pprint (db.current_op())
#pprint.pprint(collection.find_one())