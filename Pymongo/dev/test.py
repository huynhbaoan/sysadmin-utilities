#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint
import time
import os
import mylib

# client = MongoClient('mongodb://127.0.0.1:27017')
# db = client['mondra_log']
# list = db.list_collection_names()
# print ("\n\nFINAL RESULT: "+str(list))

mylib.re_arrange('GameRewardLog')