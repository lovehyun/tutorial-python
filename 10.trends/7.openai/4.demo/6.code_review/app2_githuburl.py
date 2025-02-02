import os
import re
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='')
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 테스트 URL
# https://github.com/lovehyun/tutorial-python/blob/main/11.security/1.sqli/app_weak.py
def convert_github_url_to_raw(url):
    """
    GitHub 파일 URL (예: https://github.com/user/repo/blob/branch/path/to/file.py)
    을 raw 파일 URL (예: https://raw.githubusercontent.com/user/repo/branch/path/to/file.py)로 변환합니다.
    """
    pattern = r"https://github.com/(.+)/blob/(.+)"
    match = re.match(pattern, url)
    if match:
        return f"https://raw.githubusercontent.com/{match.group(1)}/{match.group(2)}"
    return url

@app.route("/")
def index():
    # templates 폴더 내의 index.html 렌더링
    return send_from_directory(app.static_folder, 'index2.html')

@app.route("/api/check", methods=["POST"])
def check_code():
    """
    JSON 형식의 POST 요청({ "github_url": "..." })을 받아서,
    해당 URL의 소스코드를 가져오고 OpenAI API를 통해 보안 취약점 분석을 진행합니다.
    """
    data = request.get_json()
    github_url = data.get("github_url")
    if not github_url:
        return jsonify({"error": "github_url 필드가 필요합니다."}), 400

    raw_url = convert_github_url_to_raw(github_url)
    
    try:
        resp = requests.get(raw_url)
        resp.raise_for_status()
        code = resp.text
    except Exception as e:
        return jsonify({"error": f"파일을 가져오는 중 에러 발생: {e}"}), 500

    prompt = (
        "다음 소스코드에서 보안 취약점을 분석해줘.\n"
        "각 취약점에 대해 해당 코드의 라인 번호, 코드 스니펫, 취약점 설명과"
        "개선 방안을 마크다운 형식의 리스트로 출력해줘.\n\n"
        "소스코드:\n"
        "------------------------------\n"
        f"{code}\n"
        "------------------------------"
    )

    try:
        openai_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 보안 코드 분석 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        analysis = openai_response.choices[0].message.content
        print(analysis)
    except Exception as e:
        return jsonify({"error": f"ChatGPT API 호출 중 에러 발생: {e}"}), 500

    return jsonify({
        "code": code,
        "analysis": analysis
    })

if __name__ == "__main__":
    app.run(debug=True)
