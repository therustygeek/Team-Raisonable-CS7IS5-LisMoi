from pymongo import MongoClient
import json
import datetime

Client = MongoClient()
db = Client['Book']

def create_collection():
    jsonfile = open('MOCK_DATA.json','r')
    DML = json.load(jsonfile)
    collection = db['book_repository']
    collection.insert_many(DML)

def create_user_collection():
    jsonfile=open('UserInformation.json','r')
    DML=json.load(jsonfile)
    collection=db['User']
    collection.insert_many(DML)

def select_data(genre):
    result=collection.find({'genre':genre}).limit(10)
    for data in result:
        print(data)


create_user_collection()

# select_data('Comedy')