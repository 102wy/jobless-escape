import json
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import hashlib
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




@app.route('/sign_up/check_ID', methods=['POST'])
def check_ID():
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/check_nickname', methods=['POST'])
def check_nickname():
    nickname_receive = request.form['nickname_give']
    exists = bool(db.users.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/save', methods=['POST'])
def signup_save():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": id_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nickname": nickname_receive,  # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
