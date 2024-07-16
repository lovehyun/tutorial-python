# main.py

import time
from api.jsonplaceholder_api2_cache import JSONPlaceholderAPI

# API 초기화
api = JSONPlaceholderAPI()

# 1. 사용자 게시글 가져오기 (첫 번째 - API에서 가져옴)
start_time = time.time()
user_posts = api.get_posts_by_user(user_id=1)
api_time = (time.time() - start_time) * 1000
print(f"사용자 1의 게시글 (첫 번째 가져오기): {user_posts}")
print(f"소요 시간 (API): {api_time:.4f} ms")

# 첫 번째 가져온 후 캐시 확인
print("\n첫 번째 가져온 후 캐시 내용:")
api.view_cache()

# 2. 사용자 게시글 가져오기 (두 번째 - 캐시에서 가져옴)
start_time = time.time()
user_posts_cached = api.get_posts_by_user(user_id=1)
cache_time = (time.time() - start_time) * 1000
print(f"사용자 1의 게시글 (두 번째 가져오기 - 캐시에서): {user_posts_cached}")
print(f"소요 시간 (캐시): {cache_time:.4f} ms")

# 두 번째 가져온 후 캐시 확인
print("\n두 번째 가져온 후 캐시 내용:")
api.view_cache()

# 3. 새 게시글 작성 (게시글 목록 캐시 무효화됨)
new_post = api.create_post(user_id=1, title="새 게시글", body="이것은 새로운 게시글입니다.")
print("\n새 게시글 작성됨:")
print(new_post)

# 새 게시글 작성 후 캐시 확인
print("\n새 게시글 작성 후 캐시 내용:")
api.view_cache()

# 4. 기존 게시글 업데이트 (업데이트된 게시글 캐시 무효화됨)
updated_post = api.update_post(post_id=1, title="업데이트된 제목", body="업데이트된 내용입니다.")
print("\n게시글 1 업데이트됨:")
print(updated_post)

# 게시글 업데이트 후 캐시 확인
print("\n게시글 1 업데이트 후 캐시 내용:")
api.view_cache()

# 5. 게시글 삭제 (삭제된 게시글 캐시 무효화됨)
delete_status = api.delete_post(post_id=1)
print(f"\n게시글 1 삭제 상태: {delete_status}")

# 게시글 삭제 후 캐시 확인
print("\n게시글 1 삭제 후 캐시 내용:")
api.view_cache()

# 6. 첫 번째 게시글의 댓글 가져오기 (첫 번째 - API에서 가져옴)
start_time = time.time()
post_comments = api.get_comments_by_post(post_id=1)
api_time = (time.time() - start_time) * 1000
print(f"\n게시글 1의 댓글 (첫 번째 가져오기): {post_comments}")
print(f"소요 시간 (API): {api_time:.4f} ms")

# 댓글 가져온 후 캐시 확인
print("\n댓글 가져온 후 캐시 내용:")
api.view_cache()

# 7. 첫 번째 게시글의 댓글 가져오기 (두 번째 - 캐시에서 가져옴)
start_time = time.time()
post_comments_cached = api.get_comments_by_post(post_id=1)
cache_time = (time.time() - start_time) * 1000
print(f"\n게시글 1의 댓글 (두 번째 가져오기 - 캐시에서): {post_comments_cached}")
print(f"소요 시간 (캐시): {cache_time:.4f} ms")

# 두 번째 댓글 가져온 후 캐시 확인
print("\n두 번째 댓글 가져온 후 캐시 내용:")
api.view_cache()
