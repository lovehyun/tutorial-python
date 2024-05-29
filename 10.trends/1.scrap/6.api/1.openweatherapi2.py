import os
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 설정
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# API 요청을 보낼 URL과 파라미터
url = 'http://api.openweathermap.org/data/2.5/weather'
params = {
    'q': 'Seoul',  # 도시 이름
    'appid': API_KEY,  # 사용자의 API 키
    'units': 'metric',  # 섭씨로 결과를 얻기 위해 'metric' 사용
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
    print("요청에 실패하였습니다. 상태 코드:", response.status_code)
