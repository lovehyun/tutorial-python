import os
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 설정
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
if not API_KEY:
    print("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
    exit(1)

# 서울의 좌표
LAT = 37.5665
LON = 126.9780

# One Call API 요청을 보낼 URL과 파라미터
url = 'https://api.openweathermap.org/data/2.5/weather'
params = {
    'lat': LAT,
    'lon': LON,
    'appid': API_KEY,
    'units': 'metric',  # 섭씨로 결과를 얻기 위해 'metric' 사용
    'lang': 'kr'  # 한국어로 결과를 얻기 위해 'kr' 사용
}

# GET 요청 보내기
response = requests.get(url, params=params)

# 응답 확인
if response.status_code == 200:
    # JSON 데이터 가져오기
    weather_data = response.json()
    
    # 필요한 정보 추출
    city_name = weather_data['name']
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    
    # 결과 출력
    print(f"도시: {city_name}")
    print(f"온도: {temperature} C")
    print(f"날씨: {description}")
else:
    print(f"요청에 실패하였습니다. 상태 코드: {response.status_code}")
    print(f"응답 내용: {response.text}")
