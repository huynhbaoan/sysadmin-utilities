#!/usr/bin/python

import mylib
import time, datetime, calendar


BACKUP_PATTERN = 'GameRewardLog'
DIR = '/home/huynhbaoan/PythonProject/Pymongo/dev/'


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
BEGIN_MONTH = 1
BEGIN_YEAR = 2015
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
"""
for YEAR in range(BEGIN_YEAR, END_YEAR+1):
    if YEAR != END_YEAR:
        for MONTH in range(1, 13):
            mylib.compress_docs(DIR, BACKUP_PATTERN, MONTH, YEAR)
    else:
        for MONTH in range(BEGIN_MONTH, END_MONTH+1):
            mylib.compress_docs(DIR, BACKUP_PATTERN, MONTH, YEAR)