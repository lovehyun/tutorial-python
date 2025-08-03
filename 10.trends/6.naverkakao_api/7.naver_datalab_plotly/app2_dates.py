from flask import Flask, render_template, request
import requests
import plotly.graph_objs as go
import plotly.io as pio
from dotenv import load_dotenv
import os
import json

# .env 파일 로드
load_dotenv()
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index2.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("keyword")
    start_date = request.form.get("startDate")
    end_date = request.form.get("endDate")
    time_unit = request.form.get("timeUnit")

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
        "Content-Type": "application/json"
    }

    data = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,  # <-- 사용자 선택 반영
        # "timeUnit": "month",  # 또는 'date', 'week'
        "keywordGroups": [
            {
                "groupName": keyword,
                "keywords": [keyword]
            }
        ],
        "device": "pc"
    }

    res = requests.post("https://openapi.naver.com/v1/datalab/search", headers=headers, data=json.dumps(data))

    if res.status_code != 200:
        return f"API 요청 실패: {res.status_code} - {res.text}"

    result = res.json()
    data_points = result["results"][0]["data"]

    dates = [item["period"] for item in data_points]
    ratios = [item["ratio"] for item in data_points]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=ratios, mode='lines+markers', name=keyword))
    fig.update_layout(
        title=f"검색어 '{keyword}'의 검색 트렌드",
        xaxis_title="날짜",
        yaxis_title="검색 비율 (%)",
        template="plotly_white"
    )

    graph_html = pio.to_html(fig, full_html=False)

    return render_template("index2.html", graph_html=graph_html, keyword=keyword,
                           start_date=start_date, end_date=end_date, time_unit=time_unit)

if __name__ == "__main__":
    app.run(debug=True)
