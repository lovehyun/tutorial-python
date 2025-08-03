from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

AGE_GROUPS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
AGE_LABELS = {
    "1": "0-12세", "2": "13-18세", "3": "19-24세", "4": "25-29세",
    "5": "30-34세", "6": "35-39세", "7": "40-44세", "8": "45-49세",
    "9": "50-54세", "10": "55-59세", "11": "60세 이상"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword_input = request.form.get("keywords")
        if not keyword_input:
            return render_template("index2.html", error="검색어를 입력해주세요")

        keywords = [k.strip() for k in keyword_input.split(",") if k.strip()]
        start = request.form.get("startDate") or "2024-01-01"
        end = request.form.get("endDate") or "2024-12-31"
        unit = request.form.get("timeUnit") or "month"

        headers = {
            "X-Naver-Client-Id": CLIENT_ID,
            "X-Naver-Client-Secret": CLIENT_SECRET,
            "Content-Type": "application/json"
        }

        def fetch_result(payload):
            res = requests.post("https://openapi.naver.com/v1/datalab/search", json=payload, headers=headers)
            return res.json()

        # 전체 검색 추이
        keyword_groups = [{"groupName": k, "keywords": [k]} for k in keywords]
        payload_all = {
            "startDate": start,
            "endDate": end,
            "timeUnit": unit,
            "keywordGroups": keyword_groups
        }
        main_data = fetch_result(payload_all)

        if "results" not in main_data or not main_data["results"]:
            return render_template("index2.html", error="검색 결과가 없습니다. 다른 키워드를 시도해보세요.")

        # 트렌드 비중 테이블용 집계
        trend_summary = []
        for res in main_data["results"]:
            total = sum([r["ratio"] for r in res["data"]])
            trend_summary.append({"title": res["title"], "total_ratio": round(total, 2)})

        # 성별별 검색 비중
        gender_data = {}
        for gender in ["m", "f"]:
            payload_gender = dict(payload_all)
            payload_gender["gender"] = gender
            g_result = fetch_result(payload_gender)["results"]
            for i, keyword in enumerate(keywords):
                for j, item in enumerate(g_result[i]["data"]):
                    gender_data.setdefault(keyword, [])
                    if len(gender_data[keyword]) <= j:
                        gender_data[keyword].append({"period": item["period"], "ratio_male": 0, "ratio_female": 0})
                    key = "ratio_male" if gender == "m" else "ratio_female"
                    gender_data[keyword][j][key] = item["ratio"]

        # 연령대별 검색 비중
        age_data = {}
        for keyword in keywords:
            age_data[keyword] = []
            for age in AGE_GROUPS:
                payload_age = {
                    "startDate": start,
                    "endDate": end,
                    "timeUnit": unit,
                    "keywordGroups": [{"groupName": keyword, "keywords": [keyword]}],
                    "ages": [age]
                }
                result = fetch_result(payload_age)
                a_result = result.get("results", [{}])[0].get("data", [])
                total_ratio = sum(d["ratio"] for d in a_result) / len(a_result) if a_result else 0
                age_data[keyword].append({"age": AGE_LABELS[age], "ratio": round(total_ratio, 2)})

        return render_template("index2.html", result={
            "results": main_data["results"],
            "gender": gender_data,
            "age": age_data,
            "summary": trend_summary
        })

# 결과 데이터 유형
# result["results"]: 월별 전체 검색 추이 (그래프용)
# result["gender"]: 성별 비율 (남/여) - 키워드별로 분리
# result["age"]: 연령대 비율 - 키워드별로 분리
# result["summary"]: 키워드별 전체 검색량 요약 테이블

    return render_template("index2.html")

if __name__ == "__main__":
    app.run(debug=True)
