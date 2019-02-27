from pymongo import MongoClient
import json
import datetime

Client = MongoClient()
db = Client['Book']
collection = db['book_repository']

def create_collection():
    jsonfile = open('MOCK_DATA.json','r')
    DML = json.load(jsonfile)
    collection.insert_many(DML)

def select_data():
    result=collection.find({'genre':'Comedy'}).limit(10)
    for data in result:
        print(data)

select_data()

