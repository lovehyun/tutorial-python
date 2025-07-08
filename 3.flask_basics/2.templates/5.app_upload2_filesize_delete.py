from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# config 를 하나씩 설정
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# app.config['MAX_CONTENT_LENGTH'], 이 설정만 하면 Flask는
# - 파일이 업로드되기 전에 전체 요청의 Content-Length를 확인
# - 제한을 넘으면 아예 request.files에 접근하기도 전에 차단
# - werkzeug.exceptions.RequestEntityTooLarge 예외 발생 (413)
# https://flask.palletsprojects.com/en/latest/config/#MAX_CONTENT_LENGTH

# config 설정 일괄 적용
app.config.update(
    UPLOAD_FOLDER='uploads',
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif', 'pdf'},
    # MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 최대 16MB
    SECRET_KEY='my-secret-key'
)

# 업로드 폴더가 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 확장자 검사 함수
def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in app.config['ALLOWED_EXTENSIONS']

def is_file_too_large(file, max_bytes):
    # file.seek(0, os.SEEK_END)  # 파일 끝으로 이동
    # size = file.tell()  # 현재 위치(=파일 크기)
    # file.seek(0)  # 다시 처음 위치로 되돌림 (중요!)
    
    pos = file.stream.tell() # 현재 (이전 작업을 고려해서) 현재 fd의 위치를 저장
    file.stream.seek(0, os.SEEK_END) # 끝으로 이동
    size = file.stream.tell()
    file.stream.seek(pos) # 원래 위치로 돌아가라
    
    return size > max_bytes

# 업로드 폼 페이지
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload2.html', files=files)

# 파일 업로드 처리
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '파일이 전송되지 않았습니다.'

    file = request.files['file']
    if file.filename == '':
        return '파일이 선택되지 않았습니다.'
    
    # 파일 크기 제한 (예: 1MB)
    max_size = 1 * 1024 * 1024  # 1MB
    if is_file_too_large(file, max_size):
        return '파일 크기가 1MB를 초과했습니다.'

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))

    return '허용되지 않은 파일 형식입니다.'

# 파일 삭제
@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return redirect(url_for('index'))
    else:
        return '파일이 존재하지 않습니다.'


# 413 오류 처리 추가
# RequestEntityTooLarge() 발생 시에 처리되는 함수 (MAX_CONTENT_LENGTH 가 초과시 자동 발생)
@app.errorhandler(413)
def too_large(e):
    size_mb = round(app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024), 2)
    return f"업로드한 파일이 너무 큽니다. 최대 {size_mb}MB까지 허용됩니다.", 413

if __name__ == '__main__':
    app.run(debug=True)
