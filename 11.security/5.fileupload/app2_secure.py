# 해결 방법
# - 파일 확장자 검증: 안전한 확장자만 허용하도록 파일 확장자를 확인해야 합니다.
# - 파일 내용 검증: 파일이 이미지, 문서 등 특정 유형인지 확인하기 위해 파일 내용을 검증하는 라이브러리를 사용할 수 있습니다.
# - 저장 위치 및 실행 권한 제한: 업로드된 파일을 실행 불가능한 위치에 저장하거나, 실행 권한을 제한하여 악성 파일이 실행되지 않도록 해야 합니다.

from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}  # 허용 확장자 목록
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if not allowed_file(file.filename):
        return "File type not allowed", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return f"File uploaded successfully: {file.filename}"

if __name__ == "__main__":
    app.run(debug=True)
