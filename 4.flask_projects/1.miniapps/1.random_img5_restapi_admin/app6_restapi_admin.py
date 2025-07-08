from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 이미지 정보 DB (메모리 기반)
image_db = [
    {"filename": "cat1.jpg", "keywords": ["cat", "animal", "cute"]},
    {"filename": "cat2.jpg", "keywords": ["cat", "pet", "cute"]},
    {"filename": "cat3.jpg", "keywords": ["cat", "kitty", "cute"]},
    {"filename": "dog1.jpg", "keywords": ["dog", "pet", "park"]},
    {"filename": "panda1.jpg", "keywords": ["panda", "zoo", "bear"]}
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# | 기능            | HTTP 메서드 | 라우트                     | 설명                          |
# | --------------- | ---------- | -------------------------- | ----------------------------- |
# | 이미지 전체 조회 | GET        | `/api/images`              | 전체 이미지 및 키워드 반환     |
# | 이미지 검색      | GET        | `/api/images/search?q=cat` | 키워드 포함 이미지 필터링      |
# | 이미지 업로드    | POST       | `/api/images`              | 새 이미지 업로드 및 키워드 등록 |
# | 키워드 수정      | PUT        | `/api/images/<filename>`   | 해당 이미지 키워드 수정        |
# | 이미지 삭제      | DELETE     | `/api/images/<filename>`   | 이미지 삭제                   |

# HTML 서빙
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/admin")
def admin():
    return send_from_directory("static", "admin.html")

# 이미지 검색
@app.route("/api/images/search")
def search_images():
    query = request.args.get("q", "").lower()
    results = []
    for item in image_db:
        if any(query in keyword for keyword in item["keywords"]):
            results.append({
                "filename": item["filename"],
                # "url": f"/static/images/{item['filename']}",
                "url": f"/images/{item['filename']}",
                "keywords": item["keywords"]
            })
    return jsonify(results)

# 이미지 전체 조회
@app.route("/api/images")
def get_all_images():
    results = [
        {
            "filename": item["filename"],
            # "url": f"/static/images/{item['filename']}",
            "url": f"/images/{item['filename']}",
            "keywords": item["keywords"]
        } for item in image_db
    ]
    return jsonify(results)

# 업로드 허용 검사
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 이미지 업로드 (POST)
@app.route("/api/images", methods=["POST"])
def upload_image():
    file = request.files.get("image")
    keywords = request.form.get("keywords", "").lower().split(",")

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # DB에 추가
    image_db.append({
        "filename": filename,
        "keywords": [kw.strip() for kw in keywords if kw.strip()]
    })

    return jsonify({"message": "Uploaded", "filename": filename}), 201

# 키워드 수정 (PUT)
@app.route("/api/images/<filename>", methods=["PUT"])
def update_keywords(filename):
    data = request.get_json()
    new_keywords = [
        kw.strip().lower()  # 소문자로 통일
        for kw in data.get("keywords", [])
        if kw.strip()  # 공백 제거 후 still not-empty
    ]
    
    # 중복 제거도 하고 싶다면? (단, set은 순서가 바뀔 수 있음)
    # new_keywords = list(set(
    #     kw.strip().lower()
    #     for kw in data.get("keywords", [])
    #     if kw.strip()
    # ))

    for item in image_db:
        if item["filename"] == filename:
            item["keywords"] = new_keywords
            return jsonify({"message": "Keywords updated"})

    return jsonify({"error": "Image not found"}), 404

# 이미지 삭제 (DELETE)
@app.route("/api/images/<filename>", methods=["DELETE"])
def delete_image(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # 실제 파일 삭제
    # if os.path.exists(filepath):
    #     os.remove(filepath)

    # 메모리 DB에서 삭제
    global image_db
    image_db = [img for img in image_db if img["filename"] != filename]

    return jsonify({"message": "Image deleted"})

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)
