import json
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

# Flask
app = Flask(__name__)
# .env
load_dotenv()
ID = os.environ.get('DB_ID')
PW = os.environ.get('DB_PW')
# DB
client = MongoClient("mongodb+srv://"+ID+":"+PW+"@joblessescape.dvnaltz.mongodb.net/?retryWrites=true&w=majority")
db = client.joblessescape


@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')


@app.route('/signup',methods=["GET"])
def signup():
    return render_template('signup_page.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
