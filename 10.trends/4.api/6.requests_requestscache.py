# pip install requests_cache

import requests
import requests_cache

# 캐시 초기화 (10초 만료 시간)
requests_cache.install_cache('example_cache', expire_after=10)

# 첫 번째 요청 (API에서 가져옴)
response = requests.get('https://jsonplaceholder.typicode.com/posts?userId=1')
print("첫 번째 요청 (API에서):")
print(response.json())

# 두 번째 요청 (캐시에서 가져옴)
response = requests.get('https://jsonplaceholder.typicode.com/posts?userId=1')
print("두 번째 요청 (캐시에서):")
print(response.json())

# 캐시 안에 담긴 내용 출력
print("\n--- Cache contents ---")
print(requests_cache.get_cache().responses)

# 캐시 비활성화
requests_cache.uninstall_cache()
