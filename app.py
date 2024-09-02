from flask import Flask, render_template, url_for, request
from datetime import datetime 
import pymongo
from db import to_db, get_from_db, clean_house

app = Flask(__name__)

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
        content = content0, content1, content2, content3, content4, content5
        to_db(client, name, content)
    return render_template('add_client.html')
    
@app.route('/admin', methods= ('POST', 'GET'))
def admin():
    clientinfo = get_from_db('CEO Interview')
    return render_template('test.html', clientinfo = clientinfo)

if __name__ == '__main__':
    app.run(debug=True)