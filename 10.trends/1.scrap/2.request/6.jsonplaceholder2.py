# pip install requests pandas

import requests
import pandas as pd

# API 엔드포인트 URL
url = 'https://jsonplaceholder.typicode.com/users'

# API로부터 데이터 가져오기
response = requests.get(url)
data = response.json()

# 가져온 데이터 파싱하여 데이터프레임 생성
df = pd.DataFrame(data)

# 데이터프레임 출력
print(df)
