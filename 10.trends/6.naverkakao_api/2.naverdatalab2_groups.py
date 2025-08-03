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
    "endDate": "2024-12-31",
    "timeUnit": "month",  # "date", "week", "month"
    # "keywordGroups": [ # 여러 개의 검색어 그룹을 정의해서 트렌드를 비교하거나 분석하기 위한 입력 항목, groupName(그룹이름) 과 keywords(검색어리스트)
        # {"groupName": "마스크", "keywords": ["마스크"]},
        # {"groupName": "손소독제", "keywords": ["손소독제"]},
    # ],
    "keywordGroups": [ # 여러 개의 검색어 그룹을 정의해서 트렌드를 비교하거나 분석하기 위한 입력 항목, groupName(그룹이름) 과 keywords(검색어리스트)
        {"groupName": "운동화 전체", "keywords": ["운동화", "스니커즈"]},
        {"groupName": "샌들", "keywords": ["샌들"]},
        {"groupName": "부츠", "keywords": ["부츠"]},
    ],
    "device": "pc",         # "pc", "mo", "all"
    "ages": ["2", "3"],     # "1":0~12세, "2":13~18세, "3":19~24세, "4":25~29세, "5":30~34세, ... "11":60세이상
    "gender": "f"           # "m", "f" 또는 생략하면 전체
}

# 요청 보내기
url = "https://openapi.naver.com/v1/datalab/search"
response = requests.post(url, headers=headers, data=json.dumps(data))

def print_group_with_diff(title, data):
    print(f"\n[{title}]")
    previous = None
    for entry in data:
        period = entry["period"]
        ratio = entry["ratio"]
        if previous is not None:
            diff = ratio - previous
            sign = "+" if diff >= 0 else ""
            print(f"{period} → {ratio:.2f}% ({sign}{diff:.2f}p)")
        else:
            print(f"{period} → {ratio:.2f}% (초기값)")
        previous = ratio

# 결과 출력
if response.status_code == 200:
    result = response.json()
    for group in result['results']:
        group_name = group['title']
        # print(f"\n[{group_name}]")
        # for entry in group['data']:
        #     print(f"{entry['period']} → 검색 비율: {entry['ratio']:.2f}%")
        print_group_with_diff(group_name, group['data'])
else:
    print("요청 실패:", response.status_code)
    print(response.text)


# [운동화 전체]
# 2024-01-01 → 78.86% (초기값)
# 2024-02-01 → 92.58% (+13.72p)
# 2024-03-01 → 100.00% (+7.42p)
# 2024-04-01 → 99.63% (-0.37p)
# 2024-05-01 → 87.27% (-12.36p)
# 2024-06-01 → 73.55% (-13.72p)
# 2024-07-01 → 60.44% (-13.10p)
# 2024-08-01 → 63.29% (+2.84p)
# 2024-09-01 → 73.18% (+9.89p)
# 2024-10-01 → 65.02% (-8.16p)
# 2024-11-01 → 58.84% (-6.18p)
# 2024-12-01 → 48.21% (-10.63p)

# [샌들]
# 2024-01-01 → 8.78% (초기값)
# 2024-02-01 → 7.29% (-1.48p)
# 2024-03-01 → 8.78% (+1.48p)
# 2024-04-01 → 32.01% (+23.24p)
# 2024-05-01 → 67.86% (+35.85p)
# 2024-06-01 → 98.15% (+30.28p)
# 2024-07-01 → 81.46% (-16.69p)
# 2024-08-01 → 31.15% (-50.31p)
# 2024-09-01 → 6.55% (-24.60p)
# 2024-10-01 → 2.97% (-3.58p)
# 2024-11-01 → 4.08% (+1.11p)
# 2024-12-01 → 2.72% (-1.36p)

# [부츠]
# 2024-01-01 → 20.02% (초기값)
# 2024-02-01 → 15.95% (-4.08p)
# 2024-03-01 → 8.78% (-7.17p)
# 2024-04-01 → 9.02% (+0.25p)
# 2024-05-01 → 10.51% (+1.48p)
# 2024-06-01 → 9.15% (-1.36p)
# 2024-07-01 → 10.26% (+1.11p)
# 2024-08-01 → 9.02% (-1.24p)
# 2024-09-01 → 16.69% (+7.66p)
# 2024-10-01 → 23.61% (+6.92p)
# 2024-11-01 → 29.30% (+5.69p)
# 2024-12-01 → 20.77% (-8.53p)

# 운동화 전체
# 시기	요약
# 3월 최고점 (100%)	봄철 수요 피크 (개학/신학기/야외 활동)
# 6~8월 하락	샌들과 경쟁, 더운 날씨 영향
# 9~10월 반등 후 하락	가을/체육 행사 등으로 반짝 상승
# 11~12월 감소	추워지며 부츠와 샌들 외 전환 가능성

# 샌들
# 시기	요약
# 4월 이후 폭발적 증가	여름 대비 수요 시작
# 6월 최고점 (98.15%)	여름철 피크
# 7월 이후 급격한 하락	계절 종료, 9월부터 거의 0 수준
# 완벽한 계절 품목 트렌드	광고/재고 타이밍 설정에 매우 유용

# 부츠
# 시기	요약
# 1~3월 하락	겨울 종료 영향으로 관심 감소
# 4~8월 낮은 수준 유지	계절 외 시기
# 9월부터 증가 → 11월 최고점(29.30%)	가을/겨울 진입으로 관심 상승
# 12월 하락	약간 의외 — 선물 시즌/연말 대비 감소?
