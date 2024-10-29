# Security Misconfiguration
# 설명: 서버 설정을 안전하게 구성하지 않거나 기본 설정으로 운영하여, 불필요한 기능이 활성화되어 있는 경우 발생하는 취약점입니다.
# 예시: 디버그 모드를 활성화한 상태로 운영하거나, 불필요한 엔드포인트가 공개된 경우입니다.
# 해결 방법: 서버 설정을 주기적으로 점검하여 불필요한 기능이나 디버그 모드를 비활성화합니다.

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route("/")
def index():
    return "<h1>Welcome to the Homepage!</h1>"

# 관리자 페이지
@app.route("/admin")
def admin():
    # 인증 없이 관리자 페이지 접근 가능
    return "<h1>Admin Page - Sensitive Configuration Data</h1><p>Server config...</p>"

# 취약한 페이지: 예외 발생
@app.route("/crash")
def crash():
    # 강제로 예외를 발생시켜 서버 크래시 유발
    raise ValueError("An unexpected error occurred!")

if __name__ == "__main__":
    app.run(debug=True)  # 디버그 모드 활성화
