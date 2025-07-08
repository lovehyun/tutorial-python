from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

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

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").lower()
    results = []

    if query:
        for item in image_db:
            if any(query in keyword for keyword in item["keywords"]):
                image_url = url_for('static', filename=f'images/{item["filename"]}')
                results.append({
                    "filename": item["filename"],
                    "url": image_url
                })

    return render_template("index.html", query=query, results=results)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html", images=image_db)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")
    keywords = request.form.get("keywords", "")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image_db.append({"filename": filename, "keywords": keywords.lower().split(",")})
    return redirect(url_for("admin"))

@app.route("/delete/<filename>")
def delete_image(filename):
    global image_db
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # if os.path.exists(filepath):
    #     os.remove(filepath)
    image_db = [img for img in image_db if img["filename"] != filename]
    return redirect(url_for("admin"))

@app.route("/update_keywords/<filename>", methods=["POST"])
def update_keywords(filename):
    new_keywords = request.form.get("keywords", "")
    for image in image_db:
        if image["filename"] == filename:
            image["keywords"] = [kw.strip() for kw in new_keywords.split(",") if kw.strip()]
            break
    return redirect(url_for("admin"))

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
