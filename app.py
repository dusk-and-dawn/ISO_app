from flask import Flask, render_template, url_for
from datetime import datetime 
import pymongo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about', methods= ('POST', 'GET'))
def about():
    return render_template('about.html')

@app.route('/admin', methods= ('POST', 'GET'))
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)