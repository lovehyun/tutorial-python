from flask import Flask, request, render_template
import os

app = Flask(__name__)

# 파일 저장 경로 설정
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드 폴더가 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 업로드 허용 확장자 (선택)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'} # set 타입 (not dict)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file_legacy(filename):
    # 파일 이름에 '.'이 포함되어 있는지 확인
    if '.' not in filename:
        return False

    # 파일 확장자를 추출 (마지막 점 기준 오른쪽부터 최대 1회만 분리)
    ext = filename.rsplit('.', 1)[1].lower()

    # 확장자가 허용된 목록에 있는지 확인
    if ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '파일이 전송되지 않았습니다.'

    file = request.files['file']
    if file.filename == '':
        return '파일이 선택되지 않았습니다.'

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f'파일 업로드 성공: {file.filename}'

    return '허용되지 않은 파일 형식입니다.'

if __name__ == '__main__':
    app.run(debug=True)
