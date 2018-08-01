#!/usr/bin/python

import pymongo
from pymongo import MongoClient
import pprint
import time

client = MongoClient('mongodb://localhost:27017/')
db = client['mondra_log']

for COLLECTION_NAME in ['BattleReport', 'BattleUserReport', 'DeckReport', \
                        'GachaReport', 'GachaUserUnique', 'MatchReport']:
    
    for YEAR in range(2015, 2016):
        for MONTH in range(12, 13): 
            for DAY in range(1, 32): 
                if (DAY < 10):
                    FDAY = '0'+str(DAY)
                else:
                    FDAY = str(DAY)
                if (MONTH < 10):
                    FMONTH = '0'+str(MONTH)
                else:
                    FMONTH = str(MONTH)

                COLLECTION = str(COLLECTION_NAME)+'_'+str(FDAY)+'_'+str(FMONTH)+'_'+str(YEAR)
                print ("Dropping collection: "+COLLECTION)
                collection = db.drop_collection(COLLECTION)
                print ("Result: "+str(collection))
                time.sleep(0.5)

    for YEAR in range(2016, 2018):
        for MONTH in range(1, 13): 
            for DAY in range(1, 32): 
                if (DAY < 10):
                    FDAY = '0'+str(DAY)
                else:
                    FDAY = str(DAY)
                if (MONTH < 10):
                    FMONTH = '0'+str(MONTH)
                else:
                    FMONTH = str(MONTH)

                COLLECTION = str(COLLECTION_NAME)+'_'+str(FDAY)+'_'+str(FMONTH)+'_'+str(YEAR)
                print ("Dropping collection: "+COLLECTION)
                collection = db.drop_collection(COLLECTION)
                print ("Result: "+str(collection))
                time.sleep(0.5)

    for YEAR in range(2018, 2019):
        for MONTH in range(1, 4): 
            for DAY in range(1, 32): 
                if (DAY < 10):
                    FDAY = '0'+str(DAY)
                else:
                    FDAY = str(DAY)
                if (MONTH < 10):
                    FMONTH = '0'+str(MONTH)
                else:
                    FMONTH = str(MONTH)

                COLLECTION = str(COLLECTION_NAME)+'_'+str(FDAY)+'_'+str(FMONTH)+'_'+str(YEAR)
                print ("Dropping collection: "+COLLECTION)
                collection = db.drop_collection(COLLECTION)
                print ("Result: "+str(collection))
                time.sleep(0.5)


list = db.list_collection_names()
print ("\n\nFINAL RESULT: "+str(list))
