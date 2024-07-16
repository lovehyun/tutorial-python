import requests
import requests_cache
from datetime import datetime, timedelta

# 캐시 초기화 (10초 만료 시간)
requests_cache.install_cache('example_cache', expire_after=10)

# Helper function to print cache contents
def print_cache_contents():
    print("\n--- Cache contents ---")
    for key, response in requests_cache.get_cache().responses.items():
        print(f"Cached Key: {key}, URL: {response.url}")
    print("--- Cache contents end ---\n")

# GET 요청: 처음 두 번의 GET 요청은 첫 번째는 API에서 데이터를 가져오고, 두 번째는 캐시에서 데이터를 가져옵니다.
# POST, PUT, DELETE 요청: 각 요청 후 clear_cache 함수를 호출하여 캐시를 수동으로 무효화합니다.

# Helper function to clear cache
def clear_cache():
    requests_cache.get_cache().clear()
    print("Cache cleared")

# Helper function to clear cache for specific URL
def clear_cache_for_url(target_url):
    cache = requests_cache.get_cache()
    keys_to_clear = [key for key, response in cache.responses.items() if response.url == target_url]
    for key in keys_to_clear:
        del cache.responses[key]
        del cache.redirects[key]
        print(f"Cache cleared for URL: {target_url}")

# GET 요청 (캐시 적용)
url = 'https://jsonplaceholder.typicode.com/posts?userId=1'
response = requests.get(url)
print("첫 번째 요청 (API에서):")
print(response.json())
print_cache_contents()

# GET 요청 (캐시 적용)
response = requests.get(url)
print("두 번째 요청 (캐시에서):")
print(response.json())
print_cache_contents()

# POST 요청 (캐시 무효화)
post_url = 'https://jsonplaceholder.typicode.com/posts'
post_data = {
    'userId': 1,
    'title': 'New Post',
    'body': 'This is a new post.'
}
response = requests.post(post_url, json=post_data)
print("\nPOST 요청 후 응답:")
print(response.json())
clear_cache()  # 캐시 무효화
# clear_cache_for_url(url)
# clear_cache_for_url(post_url)  # 특정 URL의 캐시 무효화 (단, 이 경우 GET 요청과 URL 이 다름)
# clear_cache_for_url(f"https://jsonplaceholder.typicode.com/posts?userId={post_data['userId']}")  # 관련된 GET 요청 URL의 캐시 무효화
print_cache_contents()

# PUT 요청 (캐시 무효화)
put_url = 'https://jsonplaceholder.typicode.com/posts/1'
put_data = {
    'title': 'Updated Title',
    'body': 'Updated body content.'
}
response = requests.put(put_url, json=put_data)
print("\nPUT 요청 후 응답:")
print(response.json())
clear_cache()  # 캐시 무효화
# clear_cache_for_url(url)  # 특정 URL의 캐시 무효화
print_cache_contents()

# DELETE 요청 (캐시 무효화)
delete_url = 'https://jsonplaceholder.typicode.com/posts/1'
response = requests.delete(delete_url)
print(f"\nDELETE 요청 후 상태 코드: {response.status_code}")
clear_cache()  # 캐시 무효화
# clear_cache_for_url(url)  # 특정 URL의 캐시 무효화
print_cache_contents()

# 캐시 비활성화
requests_cache.uninstall_cache()
