#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint
import time
import datetime
import os
import mylib
import calendar



BACKUP_PATTERN = 'GameRewardLog'


"""MongoDB connection"""
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['mondra_log_restore']
collection = db[BACKUP_PATTERN]


# list = db.list_collection_names()
# print ("\n\nFINAL RESULT: "+str(list))
# pprint.pprint (db.current_op())
# pprint.pprint(collection.find_one())


#mylib.re_arrange(BACKUP_PATTERN)


print (collection.count())
### This part is used to test result after import
"""Generate cursor to find document"""
cursor = collection.find().max_scan(10)
total = 0
for docs in cursor:
    pprint.pprint(docs)
    total +=1
print ("total ",total," docs")
#####################################################