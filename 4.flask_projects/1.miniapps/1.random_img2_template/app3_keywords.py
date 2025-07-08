from flask import Flask, request, render_template, url_for
import os

app = Flask(__name__)

# 이미지 정보 DB (간단한 예시)
image_db = [
    {"filename": "cat1.jpg", "keywords": ["cat", "animal", "cute"]},
    {"filename": "cat2.jpg", "keywords": ["cat", "pet", "cute"]},
    {"filename": "cat3.jpg", "keywords": ["cat", "kitty", "cute"]},
    {"filename": "dog1.jpg", "keywords": ["dog", "pet", "park"]},
    {"filename": "panda1.jpg", "keywords": ["panda", "zoo", "bear"]}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = []

    for item in image_db:
        # found = False
        # for keyword in item["keywords"]:
        #     if query in keyword:
        #         found = True
        #         break
        #
        # if found:
        #     # 결과에 추가
        
        # pythonic 한 코드 스타일 (짧고 직관적)
        if any(query in keyword for keyword in item["keywords"]):
            # 결과에 추가
            image_url = url_for('static', filename=f'images/{item["filename"]}')
            results.append({"filename": item["filename"], "url": image_url})

    return render_template("results.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
