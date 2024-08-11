from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.ISO
ISO = db.ISO

def to_db(client, name, content):
    ISO.insert_one({'client':client, 'name':name, 'content':content})
    print(f'sent to DB: {client}, {name}, {content}')

#to_db('Era Digitalis', 'Picco', 'Bauss Boy')

def show_names():
    for document in ISO.find({}, {'_id':0, 'name':1}):
        print(document.get('name'))

show_names()