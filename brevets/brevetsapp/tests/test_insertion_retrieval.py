import nose
import os
from pymongo import MongoClient
import insertion_retrieval

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb

def test_insertRetrieval_basic():
    km = [0, 1, 2]
    open = [2, 4, 6]
    close = [5, 10, 15]
    insertion_retrieval.insert(db, km, open, close)
    entries = insertion_retrieval.retrieval(db)
    kmList = []
    oList = []
    cList = []
    for i in entries:
        kmList.append(i['km'])
        oList.append(i['open'])
        cList.append(i['close'])
    assert kmList == [0,1,2]
    assert oList == [2,4,6]
    assert cList == [5,10,15]

    