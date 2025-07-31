from dotenv import load_dotenv
from flask import Flask, redirect, request, session, render_template, url_for
import requests
import os
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "fallback-secret") # 세션 보안을 위한 시크릿 키

# 환경변수 설정
KAKAO_CLIENT_ID = os.getenv("KAKAO_REST_API_KEY")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET", "")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI") # 예: http://localhost:5000/auth/kakao/callback

# [1]	사용자 → 내 사이트 접속
# [2]	내 사이트 → 카카오 인증서버로 리디렉션
# [3]	사용자 → 카카오 로그인
# [4]	카카오 → 사용자에게 동의 화면 제공
# [5]	카카오 → Authorization Code 포함 redirect (브라우저)
# [6]	사용자 브라우저 → 콜백 URL (/auth/kakao/callback) 접속
# [7]	내 사이트 → 카카오에 토큰 요청
# [8]	카카오 → 토큰 응답 (access_token)
# [9]	내 사이트 → 사용자 정보 요청
# [10]	카카오 → 사용자 정보 응답
# [11]	세션에 사용자 정보 저장 (로그인 처리)

# 홈 페이지: 로그인 여부에 따라 표시 분기
@app.route("/")
def index():
    # [1] 사용자 → 내 사이트 접속
    user = session.get("user")
    
    # [2] 내 사이트 → 사용자 브라우저를 통해 카카오 로그인 페이지로 리디렉션
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?"
        f"response_type=code&client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}&scope=profile_nickname,profile_image"
    )
    # scope=profile_nickname,profile_image: 동의 항목이므로 미설정 시 nickname이 안 올 수 있음
    
    # redirect_url 카카오 개발자 센터에 등록
    # Kakao Developers 콘솔 접속 > Kakao Developers 로그인 > 내 애플리케이션 (앱 선택)
    # 좌측 메뉴 [제품 설정 > 카카오 로그인 > 일반] 이동
    #  - "리다이렉트 URI" 설정
    #    http://localhost:5000/auth/kakao/callback

    return render_template("index.html", user=user, kakao_auth_url=kakao_auth_url)

# [5] 네이버와 마찬가지로 Authorization Code는 사용자 브라우저를 통해 전달됨
# 콜백: 인가코드 → 토큰 → 사용자 정보 → 세션 저장
@app.route("/auth/kakao/callback")
def callback():
    # [6] 사용자 브라우저 → 콜백 URL (/auth/kakao/callback) 접속
    code = request.args.get("code")
    if not code:
        return "인가 코드가 없습니다.", 400

    # [7] 내 사이트 → 카카오에 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    # grant_type=authorization_code: 고정 값
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }

    # client_secret: 카카오 로그인에서는 선택 항목이지만 보안을 위해 사용하는 것이 좋음
    if KAKAO_CLIENT_SECRET:
        data["client_secret"] = KAKAO_CLIENT_SECRET

    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post(token_url, data=data, headers=headers).json()
    
    # [8] 카카오 → Access Token 응답
    access_token = token_res.get("access_token")

    if not access_token:
        return f"토큰 발급 실패: {token_res}", 500

    # [9] 내 사이트 → 카카오에 사용자 정보 요청
    user_info = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    
    # [10] 카카오 → 사용자 정보 응답
    print("[카카오 로그인 완료] 사용자 정보:")
    print(json.dumps(user_info, indent=2, ensure_ascii=False))

    # [11] 내 사이트 → 로그인 처리 완료 (세션에 사용자 저장)
    # 세션에 저장
    session["user"] = user_info
    session["access_token"] = access_token

    return redirect(url_for("profile"))

# 프로필 페이지
@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))
    return render_template("profile.html", user=user)

# 로그아웃
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
