from pymongo import MongoClient
import pymongo
from flask import jsonify
import base64

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
        try: 
            result.append(i['name'])
        except:
            pass
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

def get_image_to_db(data):
    if 'image' not in data: 
        return jsonify({'success':False, 'message':'no img data found'})
    base64_image = data['image']
    if base64_image.startswith('data:image/jpeg;base64,'):
        base64_image = base64_image.replace('data:image/jpeg;base64,', '')
    ISO.insert_one({'name':'img1','image': base64_image})
    return jsonify({'success': True, 'message': 'Photo uploaded successfully'})

def ret_image_from_db(name):
    obj = ISO.find({'name':name}, {'_id':0, 'image':1})
    print(list(obj)[0])
    #if obj and 'image' in obj:
    return obj['image']  # Return the Base64 image data
    #else:
    #    return None

def save_image_from_db(name, output_file):
    # Retrieve the image data from MongoDB using the name
    base64_image = ret_image_from_db(name)

    if base64_image:
        # Decode the Base64 image string
        image_data = base64.b64decode(base64_image)

        # Save the decoded image data to a file
        with open(output_file, 'wb') as file:
            file.write(image_data)

        print(f"Image saved as {output_file}")
    else:
        print("No image found for this name.")
'''
Tests etc. 
'''
#clean_house()
#show_names()
#print(get_from_db('Puppy '))
#to_db('Era Digitalis', 'Picco', 'Bauss Boy')
#print(get_clients())
#print(get_doc_from_db('test1234.txt'))
#print(ret_image_from_db('img1'))

#save_image_from_db('img1', 'testfoto1.png')