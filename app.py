from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from datetime import datetime 
import pymongo
from db import to_db, get_from_db, clean_house, get_clients, post_doc_to_db, get_image_to_db, get_all_images
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about', methods= ('POST', 'GET'))
def about():
    if request.method == 'POST':
        client = request.form['client']
        name = 'CEO Interview'
        content0 = request.form['Q1']
        content1 = request.form['Q2']
        content2 = request.form['Q3']
        content = content0, content1, content2
        to_db(client, name, content)
    return render_template('about.html')

@app.route('/addclient', methods=('POST', 'GET'))
def add_client(): 
    if request.method == 'POST':
        client = request.form['client']
        name = request.form['client']
        content0 = request.form['Q1']
        content1 = request.form['Q2']
        content2 = request.form['Q3']
        content3 = request.form['Q4']
        content4 = request.form['Q5']
        content5 = request.form['Q6']
        content6 = request.form['Q7']
        content7 = request.form['Q8']
        content = content0, content1, content2, content3, content4, content5, content6, content7
        to_db(client, name, content)
    return render_template('add_client.html')

@app.route('/begehung',methods=('POST', 'GET'))
def begehung():
    clients = get_clients()
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form.to_dict()
        get_image_to_db(data)

    return render_template('visitation.html', clients=clients)
    
@app.route('/admin', methods= ('POST', 'GET'))
def admin():
    clients = get_clients()
    if request.method == 'POST':
        selected_client = request.form.get('dropdown_option')
        clientinfo = get_from_db(selected_client)
    else:
        clientinfo = get_from_db('Dave')

    images = get_all_images()  
    
    print(f"Number of images retrieved: {len(images)}")
    if images:
        print(f"Sample image data: {images[0].keys()}")
    
    return render_template('test.html', clients = clients, clientinfo = clientinfo, images=images)

@app.route('/test', methods= ('POST', 'GET'))
def test():
    clients = get_clients()
    if request.method == 'POST':
            clientinfo = get_from_db('Weihnachtsmann')
    else: 
        clientinfo = []
        for i in clients:
            clientinfo.append(get_from_db(i))
    return render_template('active_test.html', clients = clients, clientinfo = clientinfo)

@app.route('/tag2', methods=('POST', 'GET'))
def tag2(): 
    clients = get_clients()
    # if request.method == 'GET':
    #     clients = get_clients()
    # if request.method == 'POST':
    #     file=request.files['document']
    #     if file:
    #     # Call the function to store the document
    #         description = request.form.get('description')  # Optional metadata from form
    #         document_id = post_doc_to_db(file, description=description)

    #     if document_id:
    #         print(f'File successfully uploaded with ID: {document_id}')
    #     else:
    #         print(f'Failed to upload file')

    #     return redirect(url_for('tag2'))
    return render_template('tag2.html', clients=clients)

@app.route('/q&a', methods=('POST', 'GET', 'PUT'))
def q_and_a():
    clients = get_clients()
    chosen_client = session.get('chosen_client')

    print("Current session 'chosen_client':", session.get('chosen_client'))
    print("Default chosen_client:", chosen_client)

    if 'select_client' in request.form:
        selected_option = request.form.get('dropdown_option')
        print("Selected option from form submission:", selected_option)
        if selected_option:
            session['chosen_client'] = chosen_client
            print("Session updated with 'chosen_client':", session['chosen_client'])
        return redirect(url_for('q_and_a'))
    elif 'submit_answers' in request.form:
        if 'chosen_client' not in session:
            return redirect(url_for('q_and_a'))

        # Collect answers from the form
        answers = {key: value for key, value in request.form.items() if key != 'submit_answers'}
        return redirect(url_for('q_and_a'))
    return render_template('q&a.html', clients=clients, chosen_client=chosen_client)

@app.route('/open_qs', methods=('POST', 'GET', 'PUT', 'DELETE'))
def open_qs():
    clients = get_clients()
    return render_template('open_qs.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)