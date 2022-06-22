import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
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
SECRET_KEY = os.environ.get('SECRET_KEY')
# DB
client = MongoClient(
    "mongodb+srv://" + ID + ":" + PW + "@joblessescape.dvnaltz.mongodb.net/?retryWrites=true&w=majority")
db = client.joblessescape

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
react_data = requests.get("https://www.jobkorea.co.kr/Search/?stext=react&careerType=1", headers=headers)
spring_data = requests.get("https://www.jobkorea.co.kr/Search/?stext=spring&careerType=1", headers=headers)

soup_react = BeautifulSoup(react_data.text, 'html.parser')
soup_spring = BeautifulSoup(spring_data.text, 'html.parser')

job_announcements_react = soup_react.select(
    '#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li')
job_announcements_spring = soup_spring.select(
    '#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li')

db.job_announcement_react.drop()
db.job_announcement_spring.drop()

for job_announcement_react in job_announcements_react:
    company_name = job_announcement_react.select_one('div > div.post-list-corp > a').text
    info = job_announcement_react.select_one('div > div.post-list-info > a').text.strip()
    job = job_announcement_react.select_one('div > div.post-list-info > p.etc').text
    exp = job_announcement_react.select_one('div > div.post-list-info > p.option > span.exp').text
    region = job_announcement_react.select_one('div > div.post-list-info > p.option > span.loc.long').text
    date = job_announcement_react.select_one('div > div.post-list-info > p.option > span.date').text

    doc = {
        'company_name': company_name,
        'info': info,
        'job': job,
        'exp': exp,
        'region': region,
        'date': date
    }
    db.job_announcement_react.insert_one(doc)

for job_announcement_spring in job_announcements_spring:
    company_name = job_announcement_spring.select_one('div > div.post-list-corp > a').text
    info = job_announcement_spring.select_one('div > div.post-list-info > a').text.strip()
    job = job_announcement_spring.select_one('div > div.post-list-info > p.etc').text
    exp = job_announcement_spring.select_one('div > div.post-list-info > p.option > span.exp').text
    region = job_announcement_spring.select_one('div > div.post-list-info > p.option > span.loc.long').text
    date = job_announcement_spring.select_one('div > div.post-list-info > p.option > span.date').text

    doc = {
        'company_name': company_name,
        'info': info,
        'job': job,
        'exp': exp,
        'region': region,
        'date': date
    }
    db.job_announcement_spring.insert_one(doc)


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


@app.route('/signup', methods=["GET"])
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
        print(token)

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/quiz/<index>', methods=["GET"])
def quiz(index):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(index)
        quiz_list = list(db.quiz.find({}, {'_id': False}))
        quiz_index = db.quiz.find_one({'id': index})['id']
        quiz_content = db.quiz.find_one({'id': index})['quiz']
        quiz_answer = db.quiz.find_one({'id': index})['quiz_answer']
        a = str(quiz_answer)
        print(a)

        return render_template('quiz.html', quiz_list=quiz_list, quiz_index=quiz_index, quiz_content=quiz_content,
                               quiz_answer=a)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("signup", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signup", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/quiz/savetime', methods=['POST'])
def quiz_savetime():
    time_receive = request.form['time_give']
    cookie_receive = request.form['cookie_give']
    review_receive = request.form["review_give"]
    print(cookie_receive)
    id = jwt.decode(cookie_receive, SECRET_KEY, algorithms='HS256')["id"]
    user = db.users.find_one({'id': id})

    doc = {
        "nickname": user["nickname"],
        "totaltime": int(time_receive),
        "review": review_receive
    }
    db.ranking.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/job_announcement', methods=["GET"])
def job_announcement():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        job_announcement_react_list = list(db.job_announcement_react.find({}, {'_id': False}))
        job_announcement_spring_list = list(db.job_announcement_spring.find({}, {'_id': False}))

        return render_template('job_announcement.html',
                               rows_react=job_announcement_react_list, rows_spring=job_announcement_spring_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("signup", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signup", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/ranking', methods=["GET"])
def ranking():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        rank_list = list(db.ranking.find({}, {'_id': False}))
        user_list = list(db.users.find({}, {'_id': False}))
        sort_list = sorted(rank_list, key=lambda time: (time['totaltime']))
        msg = request.args.get("msg")
        return render_template('ranking.html', msg=msg, rank_list=sort_list, user_list=user_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("signup", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signup", msg="로그인 정보가 존재하지 않습니다."))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
