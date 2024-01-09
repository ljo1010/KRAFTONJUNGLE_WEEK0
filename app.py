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
client = MongoClient("localhost", 27017)
db = client.dbtest

# JWT 토큰 생성을 위한 비밀 키 - 이 키는 비밀로 유지되어야 합니다
SECRET_KEY = 'JUNGLE'


## URL 별로 함수명이 같거나,
## route('/') 등의 주h소가 같으면 안됩니다.

@app.route('/')
def home():
   return render_template('index.html')

   
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)