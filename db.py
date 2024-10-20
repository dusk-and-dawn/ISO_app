from pymongo import MongoClient
import pymongo

client = MongoClient('localhost', 27017)
db = client.ISO
ISO = db.ISO

def to_db(client, name, content):
    ISO.insert_one({'client':client, 'name':name, 'content':content})
    print(f'sent to DB: {client}, {name}, {content}')

def get_from_db(name):
    obj = ISO.find({'name':name}, {'_id':0, 'client': 1, 'content':1})
    result = list(obj)
    return result


def show_names():
    for document in ISO.find({}, {'_id':0, 'name':1}):
        print(document.get('name'))

def clean_house():
    ISO.delete_many({})

def get_clients()-> list[dict]:
    obj = ISO.find({}, {'_id':0, 'name':1})
    result = []
    for i in obj:
        result.append(i['name'])
    return result

def post_doc_to_db(file, filename=None, description=None):
    try:
        file_data = file.read()
        if filename is None: 
            filename = file.filename
        document = {
            'filename':filename,
            'file_data': file_data,
            'description': description,
            'upload_date': pymongo.datetime.datetime.utcnow()
        }
        result = ISO.insert_one(document)
        return str(result.inserted_id)
    except Exception as e:
        print(f'error while uploading: {e}')
        return None 
    
def get_doc_from_db(filename):
    obj = ISO.find({}, {'_id':0, 'name':filename, 'file_data':1, 'description':1, 'upload_date':1})
    result = list(obj)
    return result
#clean_house()
show_names()
#print(get_from_db('Puppy '))
#to_db('Era Digitalis', 'Picco', 'Bauss Boy')
#print(get_clients())
print(get_doc_from_db('test1234.txt'))