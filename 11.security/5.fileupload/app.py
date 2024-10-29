# File Upload Vulnerabilities
# 설명: 파일 업로드 기능에서 파일의 내용이나 확장자를 검증하지 않아 악성 파일을 서버에 업로드하여 실행할 수 있는 취약점입니다.
# 예시: .php, .exe 등 실행 가능한 파일이 업로드되도록 허용해 서버에서 악성 코드를 실행할 수 있습니다.
# 해결 방법: 업로드된 파일의 확장자를 제한하고, 업로드된 파일을 서버에서 실행 불가능한 위치에 저장해야 합니다.

# 문제점
# - 파일 확장자 검증 없음: .exe, .php와 같은 서버에서 실행 가능한 파일도 업로드할 수 있습니다.
# - 파일 내용 검증 없음: 파일의 실제 내용이 안전한지 확인하지 않습니다. 공격자는 악성 스크립트를 포함한 파일을 업로드할 수 있습니다.
# - 저장 위치 제한 없음: 모든 파일이 uploads 폴더에 저장되며, 폴더 내 파일 실행 가능 여부에 따라 추가적인 공격이 가능합니다.

from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # 업로드 폴더 설정
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # 폴더가 없으면 생성

@app.route('/')
def index():
    return render_template('upload.html')  # 파일 업로드 페이지 렌더링

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # 취약한 파일 저장: 파일 검증 없이 저장
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return f"File uploaded successfully: {file.filename}"

if __name__ == "__main__":
    app.run(debug=True)
