from dotenv import load_dotenv
import os
import requests
import json

# .env 파일에서 NAVER_CLIENT_ID / SECRET 로드
load_dotenv()
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# 요청 헤더
headers = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json"
}

# 요청 바디 (JSON)
data = {
    "startDate": "2024-01-01",
    "endDate": "2024-06-30",
    "timeUnit": "month",  # "date", "week", "month"
    "keywordGroups": [ # 여러 개의 검색어 그룹을 정의해서 트렌드를 비교하거나 분석하기 위한 입력 항목, groupName(그룹이름) 과 keywords(검색어리스트)
        {"groupName": "마스크", "keywords": ["마스크"]},
        # {"groupName": "손소독제", "keywords": ["손소독제"]},
    ],
    "device": "pc",         # "pc", "mo", "all"
    "ages": ["2", "3"],     # "1":0~12세, "2":13~18세, "3":19~24세, "4":25~29세, "5":30~34세, ... "11":60세이상
    "gender": "f"           # "m", "f" 또는 생략하면 전체
}

# 요청 보내기
url = "https://openapi.naver.com/v1/datalab/search"
response = requests.post(url, headers=headers, data=json.dumps(data))

# 결과 출력
if response.status_code == 200:
    result = response.json()
    for period in result['results'][0]['data']:
        print(f"{period['period']} → 검색 비율: {period['ratio']}")
else:
    print("요청 실패:", response.status_code)
    print(response.text)


# 2024-01-01 → 검색 비율: 84.25531
# 2024-02-01 → 검색 비율: 75.74468
# 2024-03-01 → 검색 비율: 95.74468
# 2024-04-01 → 검색 비율: 100
# 2024-05-01 → 검색 비율: 82.12765
# 2024-06-01 → 검색 비율: 55.74468

# | 날짜       | 검색 비율 (%) | 의미                                       |
# | ---------- | --------- | --------------------------------------------- |
# | 2024-01-01 | 84.26%    | 1월 동안의 검색량은 최대치 대비 약 84% 수준이었음 |
# | 2024-02-01 | 75.74%    | 2월 검색량은 더 낮아짐                          |
# | 2024-03-01 | 95.74%    | 3월 검색량이 급증하여 거의 최고치에 근접         |
# | 2024-04-01 | **100%**  | **4월이 기준 기간 중 검색량이 가장 많았던 시점** |
# | 2024-05-01 | 82.13%    | 5월은 다시 소폭 하락                           |
# | 2024-06-01 | 55.74%    | 6월에는 검색량이 큰 폭으로 감소                 |
