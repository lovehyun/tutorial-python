import requests

# API 요청을 보낼 URL과 파라미터
url = 'http://api.openweathermap.org/data/2.5/weather'
params = {
    'q': 'Seoul',  # 도시 이름
    'appid': 'YOUR_API_KEY'  # 사용자의 API 키
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
    print(f"온도: {temperature} K")
    print(f"날씨: {description}")
else:
    print("요청에 실패하였습니다. 상태 코드:", response.status_code)
