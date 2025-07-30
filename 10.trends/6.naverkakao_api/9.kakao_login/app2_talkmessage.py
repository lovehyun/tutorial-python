from dotenv import load_dotenv
from flask import Flask, redirect, request, session, render_template, url_for
import requests
import os
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "fallback-secret")

# 환경변수 설정
KAKAO_CLIENT_ID = os.getenv("KAKAO_REST_API_KEY")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET", "")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

# 홈 페이지: 로그인 여부에 따라 표시 분기
@app.route("/")
def index():
    user = session.get("user")
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?"
        f"response_type=code&client_id={KAKAO_CLIENT_ID}"
        f"&redirect_uri={KAKAO_REDIRECT_URI}&scope=profile_nickname,profile_image,talk_message"
    )
    # redirect_url 카카오 개발자 센터에 등록
    # Kakao Developers 콘솔 접속 > Kakao Developers 로그인 > 내 애플리케이션 (앱 선택)
    # 좌측 메뉴 [제품 설정 > 카카오 로그인 > 일반] 이동
    #  - "리다이렉트 URI" 설정
    #    http://localhost:5000/auth/kakao/callback

    return render_template("index2.html", user=user, kakao_auth_url=kakao_auth_url)

# 콜백: 인가코드 → 토큰 → 사용자 정보 → 세션 저장
@app.route("/auth/kakao/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "인가 코드가 없습니다.", 400

    # 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }
    if KAKAO_CLIENT_SECRET:
        data["client_secret"] = KAKAO_CLIENT_SECRET

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post(token_url, data=data, headers=headers).json()
    access_token = token_res.get("access_token")

    if not access_token:
        return f"토큰 발급 실패: {token_res}", 500

    # 사용자 정보 요청
    user_info = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

     # 세션에 저장
    session["user"] = user_info
    session["access_token"] = access_token
    
    print("[카카오 로그인 완료] 사용자 정보:")
    print(json.dumps(user_info, indent=2, ensure_ascii=False))

    return redirect(url_for("index"))
    # return redirect(url_for("profile"))

# 프로필 페이지
@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))
    return render_template("profile2.html", user=user)

# 로그아웃
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# 나에게 메세지 전송
@app.route("/message")
def send_message():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("index"))

    message_template = {
        "object_type": "text",
        "text": "안녕하세요! Flask에서 보낸 자동 메시지입니다.",
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "template_object": json.dumps(message_template)
    }

    response = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=headers,
        data=payload
    )

    if response.status_code == 200:
        return "메시지를 성공적으로 전송했습니다!"
    else:
        return f"메시지 전송 실패: {response.json()}"

# 친구 목록 조회 (선택 기능)
# 앱 설정에서 친구 목록 제공 활성화, 사용자 동의 항목에 "friends" scope 추가
# 이 기능은 비즈 앱 등록 및 검수 통과 후에만 사용 가능합니다.
@app.route("/friends")
def friends():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("index"))

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        "https://kapi.kakao.com/v1/api/talk/friends",
        headers=headers
    )

    return response.json()

if __name__ == "__main__":
    app.run(debug=True)
