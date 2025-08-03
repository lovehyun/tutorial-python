from flask import Flask, render_template, request
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_labels = []
    datasets = []
    table_data = []

    if request.method == "POST":
        keywords = request.form.get("keywords")  # 쉼표로 구분된 키워드
        keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]

        headers = {
            "X-Naver-Client-Id": CLIENT_ID,
            "X-Naver-Client-Secret": CLIENT_SECRET,
            "Content-Type": "application/json"
        }

        data = {
            "startDate": "2024-01-01",
            "endDate": "2024-12-31",
            "timeUnit": "month",
            "keywordGroups": [
                {"groupName": kw, "keywords": [kw]} for kw in keyword_list
            ],
            "device": "pc"
        }

        res = requests.post("https://openapi.naver.com/v1/datalab/search", headers=headers, data=json.dumps(data))

        if res.status_code == 200:
            result = res.json()

            chart_labels = [entry["period"] for entry in result["results"][0]["data"]]

            for group in result["results"]:
                group_name = group["title"]
                ratios = [entry["ratio"] for entry in group["data"]]

                datasets.append({
                    "label": group_name,
                    "data": ratios
                })

                table_data.append({
                    "group": group_name,
                    "data": group["data"]
                })
        else:
            return f"API 요청 실패: {res.status_code} - {res.text}"

    return render_template("index.html", labels=chart_labels, datasets=datasets, table_data=table_data)

if __name__ == "__main__":
    app.run(debug=True)
