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

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login')
def login():
   msg = request.args.get("msg")
   return render_template('login.html', msg=msg)


@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/main')
def main():
   msg = request.args.get("msg")
   return render_template('main.html', msg=msg)

# [회원가입 API]
@app.route('/api/register', methods=['POST'])
def api_register():
   id_receive = request.form['id_give']
   pw_receive = request.form['pw_give']
   nickname = request.form['nickname_give']

   # 사용자 ID 중복 검사
   existing_user = db.user.find_one({'userId': id_receive})
   if existing_user:
      return render_template('register.html', msg='이미 존재하는 사용자 ID입니다.')

   # 중복된 사용자가 없으면 회원 정보 데이터베이스에 저장
   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
   doc = {
      "userId": id_receive,
      "password": pw_hash,
      "nickname": nickname
   }
   db.user.insert_one(doc)

   # 회원가입 성공, 로그인 페이지로 리디렉트
   return redirect(url_for('login'))


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
      
# 로그인 성공, main.html로 리디렉트
      return redirect(url_for('main'))
   else:
# 로그인 실패, 로그인 페이지에 에러 메시지와 함께 렌더링
      return render_template('login.html', msg='아이디/비밀번호가 일치하지 않습니다.')
   

# # [마커 생성 API]
# @app.route('/api/createMarker',methods=['GET'])
# def create_marker():

   
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)