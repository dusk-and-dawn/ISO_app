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

def get_image_to_db(data, name=None):
    if 'image' not in data: 
        return jsonify({'success': False, 'message': 'No image data found'})
    
    base64_image = data['image']
    # Handle different image formats
    for prefix in ['data:image/jpeg;base64,', 'data:image/png;base64,']:
        if base64_image.startswith(prefix):
            base64_image = base64_image.replace(prefix, '')
            break
    
    try:
        # Validate base64 data
        base64.b64decode(base64_image)
        
        # Use provided name or generate unique one
        doc_name = name if name else f'img_{pymongo.datetime.datetime.utcnow().timestamp()}'
        
        ISO.insert_one({
            'name': doc_name,
            'image': base64_image,
            'upload_date': pymongo.datetime.datetime.utcnow()
        })
        return jsonify({'success': True, 'message': 'Photo uploaded successfully', 'name': doc_name})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error processing image: {str(e)}'})

def ret_image_from_db(name):
    obj = ISO.find_one({'name': name}, {'_id': 0, 'image': 1})
    if obj and 'image' in obj:
        return obj['image']  # Return the Base64 image data
    return None

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

def get_all_images():
    try:
        # Convert cursor to list immediately to avoid cursor timeout
        images = list(ISO.find({'image': {'$exists': True}}, {'_id': 0, 'name': 1, 'image': 1, 'upload_date': 1}))
        result = []
        for img in images:
            if 'image' in img:
                # Ensure we're adding the correct data URI prefix
                img['image'] = f"data:image/jpeg;base64,{img['image']}"
                result.append(img)
        print(f"Found {len(result)} images")  # Debug print
        return result
    except Exception as e:
        print(f"Error in get_all_images: {e}")
        return []
    
def initialize_customer_to_db(client, name, content):
    ISO.insert_one({'client':client, 'name':name, 'content':content})
    ISO.insert_one({'client':str(client) + '_media', 'name':str(name) + 'media_storage', 'media_content':0})
    print(f'sent to DB: {client}, {name}, {content}')
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