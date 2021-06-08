import os
from pymongo import MongoClient

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

def insert(database, kmList, openList, closeList):
    database.tododb.remove({})  # empty collection
    for i in range(len(kmList)):
        add = {'km': kmList[i], "open": openList[i], "close": closeList[i]}
        database.tododb.insert_one(add)

def retrieval(db):
    entries = db.tododb.find()
    return entries


