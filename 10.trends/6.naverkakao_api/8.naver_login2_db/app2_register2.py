from dotenv import load_dotenv
from flask import Flask, redirect, request, session, render_template, url_for
from user_db2 import get_user_by_naver_id, save_user_if_not_exists, update_user_profile, delete_user_by_id
import requests
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET") # 세션 보안을 위한 시크릿 키

# 네이버 OAuth2 설정값
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_REDIRECT_URI = os.getenv("NAVER_REDIRECT_URI")

@app.route("/")
def index():
    # [1] 사용자 → 내 사이트 접속
    user = session.get("user") # 세션에 저장된 사용자 정보가 있으면 index.html로 전달
    return render_template("index2.html", user=user)

@app.route("/login/naver")
def login_naver():
    # [2] 내 사이트 → 사용자 브라우저를 통해 네이버 로그인 페이지로 리디렉션
    # 네이버 인증서버로 리디렉션할 URL 구성
    auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={NAVER_CLIENT_ID}"
        f"&redirect_uri={NAVER_REDIRECT_URI}&state=xyz"
    )
    # 파라미터	            설명
    # response_type=code	OAuth2 인증 코드 방식을 의미
    # client_id	            네이버 개발자 센터에서 발급받은 Client ID
    # redirect_uri	        인증 후 돌아올 콜백 URL (네이버에 등록된 URI와 일치해야 함)
    # state	                CSRF 방지를 위한 임의 문자열 (검증 용도로 사용)
    
    return redirect(auth_url)

@app.route("/naver/callback")
def naver_callback():
    # [6] 사용자 브라우저 → 내 사이트 콜백 URL 접속 (code 전달됨)
    # 네이버에서 redirect된 code, state 파라미터 수신
    code = request.args.get("code")
    state = request.args.get("state")

    # [7] 내 사이트 → 네이버에 토큰 요청
    # 인증 코드(code)를 사용해 액세스 토큰 요청
    token_url = (
        f"https://nid.naver.com/oauth2.0/token?"
        f"grant_type=authorization_code&client_id={NAVER_CLIENT_ID}"
        f"&client_secret={NAVER_CLIENT_SECRET}&code={code}&state={state}"
    )
    # 파라미터	                    설명
    # grant_type=authorization_code	인증 코드 기반 토큰 요청이라는 뜻
    # client_id	                    클라이언트 ID
    # client_secret	                클라이언트 시크릿 키
    # code	                        인증 과정에서 받은 Authorization Code
    # state	                        초기 요청에서 사용한 값과 일치해야 함

    # [8] 네이버 → Access Token 응답
    token_response = requests.get(token_url).json()
    access_token = token_response.get("access_token")

    # [9] 내 사이트 → 네이버에 사용자 정보 요청
    # 액세스 토큰을 사용하여 사용자 프로필 정보 요청
    headers = {"Authorization": f"Bearer {access_token}"}
    # 헤더: Authorization: Bearer ACCESS_TOKEN
    profile = requests.get("https://openapi.naver.com/v1/nid/me", headers=headers).json()

    # [10] 네이버 → 사용자 정보 응답
    print("Profile response:", profile)
    # 응답예시
    # {
    #     "resultcode": "00",
    #     "message": "success",
    #     "response": {
    #         "id": "unique_id",
    #         "email": "abc@naver.com", # 선택 동의시
    #         "nickname": "길동",
    #         "name": "홍길동",
    #         "profile_image": "https://..."
    #     }
    # }
    
    # [회원가입 또는 기존 사용자 확인]
    user_info = profile["response"]

    # [11] 내 사이트 → 로그인 처리 완료 (또는 회원가입 및 추가정보 요청)
    # DB에서 사용자 조회
    user = get_user_by_naver_id(user_info["id"])
    if user:
        # 이미 가입된 사용자 → 로그인 처리
        session["user"] = dict(user)
        return redirect(url_for("index"))
    else:
        # 아직 추가정보 입력 안된 사용자 → 임시 세션 저장 후 입력 페이지로 이동
        session["temp_user"] = user_info
        return redirect(url_for("signup"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    temp_user = session.get("temp_user")
    if not temp_user:
        return redirect(url_for("index"))

    if request.method == "POST":
        address = request.form.get("address")
        phone = request.form.get("phone")
        
        # nickname 이 없으면 이름으로 저장
        nickname = temp_user.get("nickname", temp_user.get("name"))
        temp_user["nickname"] = nickname

        # DB에 회원 정보 저장
        save_user_if_not_exists(temp_user, address, phone)

        # 세션 저장
        user = get_user_by_naver_id(temp_user["id"])
        session.pop("temp_user", None)
        session["user"] = dict(user)
        return redirect(url_for("index"))

    name = temp_user.get('name', None)
    email = temp_user.get('email', None)
    
    return render_template("signup2.html", name=name, email=email)

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))

    if request.method == "POST":
        new_name = request.form.get("name")
        new_nickname = request.form.get("nickname")
        new_email = request.form.get("email")
        new_phone = request.form.get("phone")
        new_address = request.form.get("address")

        # DB 업데이트
        update_user_profile(
            user["id"], new_name, new_nickname, new_email, new_phone, new_address
        )

        # 세션도 업데이트
        user["name"] = new_name
        user["nickname"] = new_nickname
        user["email"] = new_email
        user["phone"] = new_phone
        user["address"] = new_address
        session["user"] = user

        return redirect(url_for("index"))

    return render_template("edit_profile2.html", user=user)

@app.route("/delete_account")
def delete_account():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))

    user_id = user["id"]
    delete_user_by_id(user_id)
    session.clear()
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    # 세션 초기화
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
