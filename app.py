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

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
react_data = requests.get("https://www.jobkorea.co.kr/Search/?stext=react&careerType=1",headers=headers)
spring_data = requests.get("https://www.jobkorea.co.kr/Search/?stext=spring&careerType=1",headers=headers)

soup_react = BeautifulSoup(react_data.text, 'html.parser')
soup_spring = BeautifulSoup(spring_data.text, 'html.parser')


job_announcements_react = soup_react.select('#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li')
job_announcements_spring = soup_spring.select('#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li')



for job_announcement_react in job_announcements_react:
    company_name = job_announcement_react.select_one('div > div.post-list-corp > a').text
    info = job_announcement_react.select_one('div > div.post-list-info > a').text.strip()
    job = job_announcement_react.select_one('div > div.post-list-info > p.etc').text
    exp = job_announcement_react.select_one('div > div.post-list-info > p.option > span.exp').text
    region = job_announcement_react.select_one('div > div.post-list-info > p.option > span.loc.long').text
    date = job_announcement_react.select_one('div > div.post-list-info > p.option > span.date').text

    doc = {
        'company_name':company_name,
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
    return render_template('index.html')


@app.route('/job_announcement', methods=["GET"])
def job_announcement():
    job_announcement_react_list = list(db.job_announcement_react.find({}, {'_id': False}))
    job_announcement_spring_list = list(db.job_announcement_spring.find({}, {'_id': False}))

    return render_template('job_announcement.html',
                           rows_react=job_announcement_react_list, rows_spring= job_announcement_spring_list)




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
