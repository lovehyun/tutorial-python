# pip install cachetools

import requests
import cachetools
import time

# LRUCache 생성 (10초 만료 시간)
cache = cachetools.TTLCache(maxsize=100, ttl=10)
# cache = cachetools.LFUCache(maxsize=100)

def get_posts_by_user(user_id):
    cache_key = f'posts?userId={user_id}'
    if cache_key in cache:
        print("*** 캐시에서 가져옴 ***")
        return cache[cache_key]
    else:
        print("*** API에서 가져옴 ***")
        url = f'https://jsonplaceholder.typicode.com/posts'
        response = requests.get(url, params={'userId': user_id})
        response.raise_for_status()
        data = response.json()
        cache[cache_key] = data
        return data

# 첫 번째 요청 (API에서 가져옴)
start_time = time.time()
posts = get_posts_by_user(1)
print(f"소요 시간 (API): {(time.time() - start_time) * 1000:.4f} ms")
print(posts)

# 두 번째 요청 (캐시에서 가져옴)
start_time = time.time()
posts = get_posts_by_user(1)
print(f"소요 시간 (캐시): {(time.time() - start_time) * 1000:.4f} ms")
print(posts)

# 캐시 안에 담긴 내용 출력
print("\n--- Cache contents ---")
for key, value in cache.items():
    print(f"Key: {key}, Value: {value}")
