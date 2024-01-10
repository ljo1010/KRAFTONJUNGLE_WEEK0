import datetime
import hashlib

import jwt
import requests
from bs4 import BeautifulSoup
from bson import ObjectId
from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
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
   token_receive = request.cookies.get('mytoken')
   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      user_info = db.user.find_one({"userId": payload['id']})
      return render_template('main.html', user_info=user_info)
   except jwt.ExpiredSignatureError:
      return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
   except jwt.exceptions.DecodeError:
      return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

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
   
   # nickname 중복 검사
   existing_user = db.user.find_one({'nickname': nickname})
   if existing_user:
      return render_template('register.html', msg='이미 존재하는 nickname입니다.')   

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
      
# 로그인 성공, 응답 객체 생성
      response = make_response(redirect(url_for('main')))
      # 쿠키에 토큰 설정
      response.set_cookie('mytoken', token)

      return response
   else:
      # 로그인 실패, 로그인 페이지에 에러 메시지와 함께 렌더링
      return render_template('login.html', msg='아이디/비밀번호가 일치하지 않습니다.')
   
@app.route('/logout')
def logout():
   response = make_response(redirect(url_for('login')))
   response.delete_cookie('mytoken')  # JWT 토큰 쿠키를 삭제합니다.
   return response


# [마커 생성 API]
@app.route('/api/createMarker',methods=['POST'])
def create_marker():
   data = list(db.total.find({}, {'_id': 0}))
   return jsonify({'result': 'success','data_list':data})


# [ 음식점 ID 받아서 정보넘겨 주기 API]
@app.route('/api/getRestaurantData', methods=['POST'])
def get_restaurant_data():
   # 클라이언트로부터 음식점 ID 받기
   place_name = request.json.get('place_name')

   # TODO: 음식점 ID를 사용하여 데이터베이스에서 음식점 정보 가져오기
   restaurant_data = db.total.find_one({'placename': place_name})

   # 응답 데이터 생성 및 전송
   response_data = {
      'place_name': place_name,
      'reviewcount': restaurant_data.get('reviewcount', 0)
   }

   return jsonify(response_data)


# [클라이언트로 받은 리뷰,별점 데이터에 저장]
@app.route('/api/submitReview', methods=['POST'])
def submit_review():
   # 클라이언트로부터 음식점 이름, 평점, 코멘트 받기
   data = request.json
   placename = data.get('place_name')
   rating = data.get('rating')
   comment = data.get('comment')

   # 음식점이 존재하는지 확인
   existing_doc = db.review.find_one({'placename': placename})

   if existing_doc:
      # 음식점이 이미 존재하는 경우, 리뷰 추가
      db.review.update_one(
            {'placename': placename},
            {'$push': {'reviews': {'rating': rating, 'comment':
               
               comment}}}
      )
      db.total.update_one(
         {'placename':placename},
         {'$inc':{'reviewcount':1}}
      )
   else:
      # 음식점이 없는 경우, 새로운 도큐먼트 추가
      new_doc = {
            'placename': placename,
            'reviews': [{'rating': rating, 'comment': comment}]
      }
      db.review.insert_one(new_doc)

   return jsonify({'result': 'success'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)