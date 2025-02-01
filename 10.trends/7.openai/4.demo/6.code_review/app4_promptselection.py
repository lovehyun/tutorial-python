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

def convert_github_url_to_raw(url):
    pattern = r"https://github.com/(.+)/blob/(.+)"
    match = re.match(pattern, url)
    if match:
        return f"https://raw.githubusercontent.com/{match.group(1)}/{match.group(2)}"
    return url

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index4.html')

@app.route("/api/check", methods=["POST"])
def check_code():
    data = request.get_json()
    github_url = data.get("github_url")
    vulnerability_types = data.get("vulnerability_types", [])

    if not github_url:
        return jsonify({"error": "github_url 필드가 필요합니다."}), 400

    raw_url = convert_github_url_to_raw(github_url)
    try:
        resp = requests.get(raw_url)
        resp.raise_for_status()
        code = resp.text
    except Exception as e:
        return jsonify({"error": f"파일을 가져오는 중 에러 발생: {e}"}), 500

    # 취약점 유형이 선택되었으면 리스트를 문자열로 변환
    vuln_text = ""
    if vulnerability_types:
        vuln_text = "분석 대상 취약점 유형: " + ", ".join(vulnerability_types) + "\n\n"

    # 번호가 매겨진 소스코드를 사용하고 싶다면, 미리 번호를 붙여도 됨 (여기서는 프론트엔드에 원본을 보내므로 프롬프트에선 원본 사용)
    prompt = (
        f"다음 소스코드에서 보안 취약점을 분석해줘.\n"
        f"각 취약점에 대해 해당 코드의 라인 번호, 코드 스니펫, 취약점 설명과 개선 방안을 마크다운 형식의 리스트로 출력해줘. 주석 코드는 무시해도 돼.\n\n"
        f"{vuln_text}"
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
        return jsonify({"error": f"ChatGPT API 호출 중 에러 발생: {e}"}), 500

    return jsonify({
        "code": code,
        "analysis": analysis
    })

if __name__ == "__main__":
    app.run(debug=True)
