#!/usr/bin/python

"""
Purpose: Cut log every month
Author: @quang.nv
Dependency: egenix-mx-base (easy_install egenix-mx-base)
"""

import datetime
import os
import mx.DateTime as dt
import subprocess
import pymongo
import calendar
from datetime import date, timedelta
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys
from distutils.dir_util import copy_tree
import shutil

backup_path = '/home/nguyendinhhai/Downloads/mongo/Script/backup/'
mongodump_path = '/usr/bin/mongodump'
mongo_path = '/usr/bin/mongo'
collections = ['GiftAL_201602']
database = 'GiftAL_201602'
client = MongoClient()
db   = client['GiftAL_201602']
dbnames = client.database_names()
operation= 'copy'

def db_connection():
  print "==========CHECK CONNECTED TO DATABASES=========="
  if 'GiftAL_201602' in dbnames:
    print "Connected successfully"
  else:
    print "Connection Failed"
    sys.exit(1)
  print "*********END CHECK CONNECTED TO DATABASES*********"  

def get_timestamp():
  month = 1
  year = 2016
  last_day = 31
  timestamp_from = datetime.datetime(int(year), int(month), 1, 0, 0, 0, 0) #datetime.datetime(2017, 2, 1, 0, 0)
  timestamp_to = datetime.datetime(int(year), int(month), int(last_day), 23,59,59,999) #datetime.datetime(2017, 2, 28, 23, 59, 59, 999)
  timestamp_middle = (timestamp_from.date() + (timestamp_to - timestamp_from)/2) #1452877200
  current_month = datetime.datetime(int(year), int(month), 1).strftime("%Y_%m") # '2017_02'
  print "First time stamp: %s" %timestamp_from #First time stamp: 2016-01-01 00:00:00
  print "Middle day      : %s" % (timestamp_from.date() + (timestamp_to - timestamp_from)/2) #2016-01-16
  print "Last time stamp : %s" %timestamp_to    #Last time stamp: 2016-01-31 23:59:59.000999
  return int(timestamp_from.strftime("%s")) * 1000, int(timestamp_middle.strftime("%s")) * 1000, int(timestamp_to.strftime("%s")) * 1000, current_month
  
def count_document(col, ts_first, ts_middle, ts_last, folder_name):
  print "==========INFORMATION TIMESTAMP=========="
  print "Timestamp first  : %r" %ts_first
  print "Timestamp Middle: %r" %ts_middle
  print "Timestamp last    : %r" %ts_last
  print "*********END TIMESTAMP*********"

  print "==========STEP COUNT AND DELETE DOCUMENT=========="

  query_1 = {"createdAt": { '$gte': + int(ts_first), '$lte' : + int(ts_last)}}
  result_1 = db[col].find(query_1).count()
  print "Step 1: So luong document first-date - last-date: %d"  %result_1
  if (result_1 == 0):
    print "Document empty"
    return 0

  if (result_1 <= 30e6):
    print "+ So luong document nho hon 10e6, tien hanh xoa %d document." % result_1
    if (result_1 > 0):
      run_backup(col, str(ts_first),str(ts_last), folder_name)
      remove_data(col, str(ts_first),str(ts_last))
  
    else:
      print "+ So luong document lon hon 10e6 [%s], tien hanh xoa tu first - middle va middle - last" %result_1
      query_2 = {"createdAt": {'$gte': + int(ts_first), '$lt': + int(ts_middle)}}
      result_2 = db[col].find(query_2).count()
      print "Step 2: So luong document first-date - middle-date: %s" % result_2
      print "+ So luong document lon hon 10e6 [%s], tien hanh xoa tu first - middle va middle - last" %result_1

      if (result_2 <= 30e6):
        print "+ So luong document nho hon 10e6, tien hanh xoa %d document." % result_2
        run_backup(col, str(ts_first),str(ts_middle), folder_name)
        remove_data(col, str(ts_first),str(ts_middle))
    
      else:
        print "+ So luong document lon hon 10e6 [%s], nen xoa bang tay!" %result_2
        query_3 = {"createdAt": {'$gte': + int(ts_middle), '$lt': + int(ts_last)}}
        result_3 = db[col].find(queryts_from_3).count()
        print "Step 3: So luong document middle-date - last-date: %d" % result_3

        if (result_3 <= 30e6):
          print "+ So luong document nho hon 10e6, tien hanh xoa %d document." % result_3
          run_backup(col, str(ts_middle),str(ts_last), folder_name)
          remove_data(col, str(ts_middle),str(ts_last))
        else:
          print "+ So luong document lon hon 10e6 [%s] nen xoa bang tay!" %result_3  
  return 1

def run_backup(col, ts_from, ts_to, folder_name):
  print "==========BACKUP DOCUMENT =========="
  this_backup = os.path.join(backup_path, folder_name)
  if not os.path.exists(this_backup):
    os.mkdir(this_backup)
    print('Created new backup: %s' % this_backup)
  
  query = '{\"createdAt\": {$gte: ' + ts_from + ', $lte: ' + ts_to +'}}'
  subprocess.call([mongodump_path, '--db', database, '--collection', col, '--out', this_backup, '--query', query])
  subprocess.call(["/bin/mv", this_backup+"/"+database+"/"+col+".bson", this_backup+"/"+database+"/"+col+"_"+ts_to+".bson"])
  subprocess.call(["/bin/mv", this_backup+"/"+database+"/"+col+".metadata.json", this_backup+"/"+database+"/"+col+"_"+ts_to+".metadata.json"])
  print "Query backup from first-date to last-date: %s" % query
  print "*********END BACKUP DOCUMENT *********"  

def remove_data(col, ts_from, ts_to):
  print "==========DELETE DOCUMENT =========="
  print "collection: " + col
  print "query: {'createdAt': {'$gte': " + ts_from + ", '$lte': " + ts_to + "}}" 

  db[col].delete_many({"createdAt": {'$gte': + int(ts_from), '$lte': + int(ts_to)}})

  print "==========END DELETE DOCUMENT =========="

def main():
  """
  Test Connection Mongodb
  """
  db_connection()
  """
  First get timestamp for query (month ago, from 00:00:00 01/month/year to 23:59:59 29/30/31/month/year)
  """
  timestamp_from, timestamp_middle, timestamp_to, current_month = get_timestamp()
  
  """
  Process backup all collections of Mongodb:
  """
  for collection in collections:
    count_document(collection, str(timestamp_from), str(timestamp_middle), str(timestamp_to), current_month)

if __name__ == '__main__':
  main()