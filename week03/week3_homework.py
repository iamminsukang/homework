import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

# MongoDB 커넥션 생성
client = MongoClient("mongodb://localhost:27017/")
db = client.dbsparta

# Data 요청
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
data = requests.get(url="https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713",
                    headers=headers)

# HTML Parsing & 테이블 정보 변수 생성
soup = BeautifulSoup(data.text, "html.parser")

songs = soup.select("#body-content > div.newest-list > div > table > tbody > tr")

# 랭킹, 제목, 가수명 추출해서 DB에 저장
for song in songs:
    rank = re.findall(r"\d+", song.select_one("td.number").text.strip().split(" ")[0])[0]
    title = song.select_one("td.info > a.title.ellipsis").text.strip()
    artist = song.select_one("td.info > a.artist.ellipsis").text.strip()

    doc = {
        "rank": rank,
        "title": title,
        "artist": artist
    }

    db.music_chart.insert_one(doc)


