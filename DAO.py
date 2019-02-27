#
# Databse Access Object
#
import pymongo, json


jsonfile = open('MOCK_DATA.json','r')
DML = json.load(jsonfile)
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client["book_repository"]
collection = db.book
collection.insert(DML)
