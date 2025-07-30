from dotenv import load_dotenv
from flask import Flask, redirect, request, session, render_template, url_for
import requests
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET")

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_REDIRECT_URI = os.getenv("NAVER_REDIRECT_URI")

@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/login/naver")
def login_naver():
    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={NAVER_CLIENT_ID}"
        f"&redirect_uri={NAVER_REDIRECT_URI}&state=xyz"
    )
    return redirect(auth_url)

@app.route("/naver/callback")
def naver_callback():
    code = request.args.get("code")
    state = request.args.get("state")

    token_url = (
        f"https://nid.naver.com/oauth2.0/token?"
        f"grant_type=authorization_code&client_id={NAVER_CLIENT_ID}"
        f"&client_secret={NAVER_CLIENT_SECRET}&code={code}&state={state}"
    )

    token_response = requests.get(token_url).json()
    access_token = token_response.get("access_token")

    # 사용자 정보 요청
    headers = {"Authorization": f"Bearer {access_token}"}
    profile = requests.get("https://openapi.naver.com/v1/nid/me", headers=headers).json()

    print("Profile response:", profile)

    session["user"] = profile["response"]
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
