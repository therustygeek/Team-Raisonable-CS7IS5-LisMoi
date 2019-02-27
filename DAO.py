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
    collection = db['book_repository']
    result=collection.find({'genre': genre}).limit(10)
    for data in result:
        print(data)

def update_preferences(UserId, preferences):
        collection = db['User']
        collection.update_one({'_id':UserId},{ '$set' : {'preference':preferences}})
        
def get_user_preferences(UserId):
        collection = db['User']
        preflist = collection.find_one({'_id': UserId},{'preference' : 1})
        return preflist['preference']

def print_pref(UserId):
        pref = get_user_preferences(UserId)
        if type(pref) is list: 
                for p in pref:
                        print(p)
        else: 
                print(pref)


def get_Mood(UserId):
        collection = db['User']
        moodlist = collection.find_one({'_id': UserId}, {'Mood': 1})
        return moodlist['Mood']

def set_Mood(UserId, moods):
        collection = db['User']
        collection.update_one({'_id':UserId}, {'$set': {'Mood': moods}})

def add_bookToList(UserId, BookId):
        collection = db['User']
        collection.update_one({'_id': UserId}, {'$push': {'BookList': {'$each' : BookId }}})

def remove_book(UserId, BookId):
        collection = db['User']
        collection.update_one({'_id':UserId}, {'$pull': {'BookList': {'$in': BookId }}})

#Tests
#add_bookToList(1,[1,2,3,4,5])
#remove_book(1,[2,3])
#print(get_Mood(1))
#set_Mood(1,['Happy','Normal','Scary'])
#print(get_Mood(1))
#create_user_collection()
#update_preferences(1,['Horror','Fantasy','Romance','Zombie-Apocalypse'])
#select_data('Comedy')
#print_pref(1)