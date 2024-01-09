import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MongoDB 클라이언트 설정
client = MongoClient("mongodb://team5:team5@13.125.172.222", 27017)
db = client.dbtest


db.total.delete_many({})


url = 'https://dapi.kakao.com/v2/local/search/category.json'

params1 = {'category_group_code' : 'FD6',
           'rect':'127.0414740874863,37.297405923262204,127.04699024655676,37.29892210891747',
           'page':1}

params2 = {'category_group_code' : 'FD6',
           'rect':'127.0414740874863,37.297405923262204,127.04699024655676,37.29892210891747',
            'page':2 }


params3 = {'category_group_code' : 'FD6',
           'rect':'127.0414740874863,37.297405923262204,127.04699024655676,37.29892210891747',
            'page':3 }

params4 = {'category_group_code' : 'FD6',
           'rect':'127.0414740874863,37.297405923262204,127.04699024655676,37.29892210891747',
            'page':4 }



headers = {"Authorization": "KakaoAK 8d61961ba50195955fc28aad2b263489"}
total1= requests.get(url, params=params1, headers=headers).json()['documents']
total2= requests.get(url, params=params2, headers=headers).json()['documents']
total3= requests.get(url, params=params3, headers=headers).json()['documents']
total4= requests.get(url, params=params4, headers=headers).json()['documents']


total=total1+total2+total3+total4



for i in range(0,len(total)-1):
    placename=total[i]['place_name']
    lat=total[i]['x']
    lng=total[i]['y']
    address=total[i]['road_address_name']
    place_url=total[i]['place_url']

    doc = {
        'placename' : placename,
        'lat' : lat,
        'lng' : lng,
        'road_addresss_name' : address,
        'place_url' : place_url
    }
    db.total.insert_one(doc)















