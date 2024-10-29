# 해결 방법: 리디렉션 URL을 내부 경로로 제한하거나, 허용된 URL만 리디렉션할 수 있도록 검증하는 것입니다.

from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/login')
def login():
    next_page = request.args.get('next')
    # 안전한 리디렉션을 위해 내부 URL만 허용
    if next_page and next_page.startswith('/'):
        return redirect(next_page)
    return "Login Page"

if __name__ == "__main__":
    app.run(debug=True)
