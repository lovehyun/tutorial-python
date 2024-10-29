# Security Misconfiguration
# 이 취약점은 서버의 설정이 안전하지 않게 구성되어 불필요한 정보가 노출되는 경우 발생합니다. 예를 들어, 디버그 모드가 활성화된 상태로 운영되거나 관리자 페이지가 인증 없이 노출되는 경우입니다.
# 취약한 코드 예제 (디버그 모드 활성화 및 관리자 페이지 노출)

from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route("/")
def index():
    return "<h1>Welcome to the Homepage!</h1>"

# 관리자 페이지 (세션에 관리자인 경우에만 접근 가능)
@app.route("/admin")
def admin():
    if session.get('is_admin'):
        return "<h1>Admin Page - Sensitive Configuration Data</h1><p>Server config...</p>"
    return redirect(url_for("index"))

# 취약한 페이지: 예외 발생
@app.route("/crash")
def crash():
    # 강제로 예외를 발생시켜 서버 크래시 유발
    raise ValueError("An unexpected error occurred!")

if __name__ == "__main__":
    app.run()  # 운영 환경에서는 debug=True를 제거하여 디버그 모드를 비활성화
