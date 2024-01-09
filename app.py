import datetime
import hashlib

import jwt
import requests
from bs4 import BeautifulSoup
from bson import ObjectId
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient

# Flask 애플리케이션 초기화
app = Flask(__name__)

# MongoDB 클라이언트 설정
client = MongoClient("mongodb://team5:team5@13.125.172.222", 27017)
db = client.dbtest

# JWT 토큰 생성을 위한 비밀 키 - 이 키는 비밀로 유지되어야 합니다
SECRET_KEY = 'JUNGLE'


## URL 별로 함수명이 같거나,
## route('/') 등의 주h소가 같으면 안됩니다.

@app.route('/')
def home():
   return render_template('index.html')

# [회원가입 API]
@app.route('/api/register', methods=['POST'])
def api_register():
   id_receive = request.form['id_give']
   pw_receive = request.form['pw_give']
   nickname = request.form['nickname_give']

   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

   doc = {
      "userId": id_receive,  # 아이디
      "password": pw_hash,  # 비밀번호
      "nickname": nickname  # 닉네임
   }

   db.user.insert_one(doc)

   return jsonify({'result': 'success'})

# [로그인 API]
@app.route('/api/login', methods=['POST'])
def api_login():
   id_receive = request.form['id_give']
   pw_receive = request.form['pw_give']
   
   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
   
   result = db.user.find_one({'userId': id_receive, 'password': pw_hash})
   
   if result is not None:
      payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 1)
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      
      return jsonify({'result': 'success', 'token': token})
   else:
      return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
   
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)