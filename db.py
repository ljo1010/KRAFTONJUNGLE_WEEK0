import requests
import json
from bs4 import BeautifulSoup

url = 'http://ip-api.com/json'
data = requests.get(url)

res = data.json()

url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

params1 = {'query' : '광교역 맛집', 'y' : res['lon'], 'x' :  res['lat'],'page': 1,'category_group_code' : 'FD6'}
params2 = {'query' : '광교역 맛집', 'y' : res['lon'], 'x' :  res['lat'],'page': 2,'category_group_code' : 'FD6'}
params3 = {'query' : '광교역 맛집', 'y' : res['lon'], 'x' :  res['lat'],'page': 3,'category_group_code' : 'FD6'}



headers = {"Authorization": "KakaoAK 8d61961ba50195955fc28aad2b263489"}
total1 = requests.get(url, params=params1, headers=headers).json()['documents']
total2 = requests.get(url, params=params2, headers=headers).json()['documents']
total3 = requests.get(url, params=params3, headers=headers).json()['documents']


total=total1+total2+total3


for i in range(0,len(total)-1):
    placename=total[i]['place_name']
    lat=total[i]['x']
    lng=total[i]['y']













