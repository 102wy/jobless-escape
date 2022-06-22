import json
from flask import Flask, render_template, request, jsonify , redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import jwt
import os
import hashlib
from datetime import datetime, timedelta
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

SECRET_KEY = 'SPARTA'


@app.route('/', methods=["GET"])
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("signup", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signup", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/signup',methods=["GET"])
def signup():
    msg = request.args.get("msg")
    return render_template('signup_page.html', msg=msg)


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


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=3600)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
