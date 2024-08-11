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
        client = 'testClient'
        name = request.form.get('Wie viele Angestellte arbeiten in Ihrer Firma?')
        content = 'testContent'
        to_db(client, name, content)
    return render_template('about.html')

@app.route('/admin', methods= ('POST', 'GET'))
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)