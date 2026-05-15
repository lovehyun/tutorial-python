import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

# 환경변수 로드 (.env)
load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='')
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route("/")
def index():
    # public 폴더 안의 index.html을 반환
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/check", methods=["POST"])
def check_code():
    data = request.get_json()
    code = data.get("code", "")
    if not code:
        return jsonify({"error": "소스코드가 입력되지 않았습니다."}), 400

    prompt = (
        "다음 소스코드에서 보안 취약점을 분석해줘.\n"
        "각 취약점에 대해 해당 코드의 라인 번호, 코드 스니펫, 취약점 설명과 개선 방안을 간단하게 설명해줘. 주석은 무시해도 돼.\n\n"
        "소스코드:\n"
        "------------------------------\n"
        f"{code}\n"
        "------------------------------"
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 보안 코드 분석 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        analysis = response.choices[0].message.content
    except Exception as e:
        analysis = f"분석 중 에러 발생: {str(e)}"
    return jsonify({"analysis": analysis})

if __name__ == "__main__":
    app.run(debug=True)
