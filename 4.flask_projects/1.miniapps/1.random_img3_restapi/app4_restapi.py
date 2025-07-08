from flask import Flask, request, jsonify, url_for, send_from_directory
# from flask_cors import CORS

# static_folder	    실제 파일이 저장된 디렉토리 경로
# static_url_path	URL 상에서 정적 파일을 불러올 때 사용하는 경로(prefix)
app = Flask(__name__, static_url_path='', static_folder='static')
# CORS(app)  # 모든 origin 허용 (개발 시 편의 목적)

# 간단한 이미지 DB
image_db = [
    {"filename": "cat1.jpg", "keywords": ["cat", "animal", "cute"]},
    {"filename": "cat2.jpg", "keywords": ["cat", "pet", "cute"]},
    {"filename": "cat3.jpg", "keywords": ["cat", "kitty", "cute"]},
    {"filename": "dog1.jpg", "keywords": ["dog", "pet", "park"]},
    {"filename": "panda1.jpg", "keywords": ["panda", "zoo", "bear"]}
]

# / 에서 index.html 반환
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# 이미지 검색 REST API
@app.route("/api/search")
def search_images():
    query = request.args.get("q", "").lower()
    results = []

    for item in image_db:
        if any(query in keyword for keyword in item["keywords"]):
            image_url = url_for('static', filename=f'images/{item["filename"]}', _external=True)
            results.append({
                "filename": item["filename"],
                "url": image_url
            })

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
