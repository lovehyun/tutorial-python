from flask import Flask, render_template
from flask import request, jsonify

from pymongo import MongoClient
from bson.objectid import ObjectId

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.board
collection = db.movie
auto_img = True

def get_movie_img(url):
    # 타겟 URL을 읽어서 HTML를 받아오고,
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    img_url = None
    try:
        poster = soup.select_one('.poster > a > img')
        # print(poster)
        img_url = poster['src']
    except:
        pass

    return img_url


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def create():
    rank = request.form['rank']
    title = request.form['title']
    score = request.form['score']
    url = request.form['url']

    img = None
    if auto_img is True:
        img = get_movie_img(url)

    data = {'rank':rank, 'title':title, 'score':score, 'url':url, 'img':img}
    collection.insert_one(data)

    return jsonify({'result': 'success'})

@app.route('/show', methods=['GET'])
def show():
    result = list(collection.find())
    print(result)
    for r in result:
        r["id"] = str(r["_id"])
        del r["_id"]

    print(result)

    return jsonify(result)

@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    print("id:", id)

    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({'result': 'success'})

@app.route('/modify', methods=['POST'])
def modify():
    rank = request.form['rank']
    title = request.form['title']
    score = request.form['score']
    url = request.form['url']
    id = request.form['id']

    collection.update_one({"_id": ObjectId(id)}, {'$set':{"rank":rank, "title":title, "score":score, "url":url}})

    return jsonify({'result': 'success'})

@app.route('/clear')
def clear():
    collection.drop()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
