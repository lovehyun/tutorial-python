# Flask에서 정적 파일(예: CSS, JavaScript, 이미지 파일 등)을 제공하려면 static 폴더를 사용하면 됩니다. 
# Flask는 기본적으로 static 폴더에 있는 파일을 자동으로 서비스합니다.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
