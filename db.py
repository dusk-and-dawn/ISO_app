from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ISO
ISO = db.ISO

def to_db(client, name, content):
    ISO.insert_one({'client':client, 'name':name, 'content':content})
    print(f'sent to DB: {client}, {name}, {content}')

#to_db('Era Digitalis', 'Picco', 'Bauss Boy')

def show_names():
    for document in ISO.find({}, {'_id':0, 'client': 1, 'name':1, 'content':1}):
        print(document.get('client'))
        print(document.get('name'))
        print(document.get('content'))

def clean_house():
    ISO.delete_many({})

#clean_house()
#show_names()