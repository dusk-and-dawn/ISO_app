from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ISO
ISO = db.ISO

def to_db(client, name, content):
    ISO.insert_one({'client':client, 'name':name, 'content':content})
    print(f'sent to DB: {client}, {name}, {content}')

#to_db('Era Digitalis', 'Picco', 'Bauss Boy')

def get_from_db(name):
    return ISO.find({'name':name}, {'_id':0, 'client': 1, 'content':1})


def show_names():
    for document in ISO.find({}, {'_id':0, 'name':1}):
        print(document.get('name'))

def clean_house():
    ISO.delete_many({})

#clean_house()
show_names()