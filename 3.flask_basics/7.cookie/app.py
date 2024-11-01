from flask import Flask, request, make_response

app = Flask(__name__)

# 쿠키 설정하기
@app.route("/set-cookie")
def set_cookie():
    response = make_response("Cookie has been set!")
    response.set_cookie("my_cookie", "cookie_value")  # 쿠키 설정
    return response

# 쿠키 읽기
@app.route("/get-cookie")
def get_cookie():
    cookie_value = request.cookies.get("my_cookie")  # 쿠키 읽기
    if cookie_value:
        return f"Cookie value: {cookie_value}"
    else:
        return "No cookie found!"

if __name__ == "__main__":
    app.run(debug=True)
