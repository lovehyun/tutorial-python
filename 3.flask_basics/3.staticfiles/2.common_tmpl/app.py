from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/user")
def user():
    return render_template("user.html")

# 관리자 페이지 리라우트
@app.route('/admin')
def admin():
    # if 로그인 안한 사용자면? 홈으로 돌려보내기 를 구현해야함.
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
