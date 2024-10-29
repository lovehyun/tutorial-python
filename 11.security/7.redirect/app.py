# Unvalidated Redirects and Forwards
# 설명: 사용자가 URL 파라미터에 따라 외부 사이트로 리디렉션될 수 있는 경우, 공격자는 사용자를 피싱 페이지로 유도할 수 있습니다.
# 예시: 로그인 후 next 파라미터에 따른 리디렉션을 허용할 때 http://malicious-site.com으로 유도할 수 있습니다.
# 해결 방법: 리디렉션 시 허용된 URL만 리디렉션할 수 있도록 검증합니다.

# 문제점: next 파라미터 값으로 외부 URL을 입력하면 로그인 후 해당 URL로 리디렉션됩니다. 공격자는 http://localhost:5000/login?next=http://malicious-site.com 같은 URL을 만들어 사용자를 피싱 사이트로 유도할 수 있습니다.

from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/login')
def login():
    # next 파라미터를 통해 리디렉션
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)
    return "Login Page"

if __name__ == "__main__":
    app.run(debug=True)
