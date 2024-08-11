from flask import Flask, render_template, url_for, request
from datetime import datetime 
import pymongo
from db import to_db

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

@app.route('/admin', methods= ('POST', 'GET'))
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)