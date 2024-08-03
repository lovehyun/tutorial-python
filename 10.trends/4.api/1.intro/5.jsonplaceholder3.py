import requests

# 1. 특정 사용자 ID를 기준으로 게시글을 가져옵니다.
user_id = 1
url = f'https://jsonplaceholder.typicode.com/posts?userId={user_id}'
response = requests.get(url)
posts_data = response.json()

# 게시글 데이터를 출력합니다.
print("Posts by user 1:")
for post in posts_data:
    print(post)

# 2. 게시글 ID를 기준으로 첫 번째 게시글의 댓글을 가져옵니다.
post_id = 1
url = f'https://jsonplaceholder.typicode.com/posts/{post_id}/comments'
response = requests.get(url)
comments_data = response.json()

# 댓글 데이터를 출력합니다.
print("\nComments for post 1:")
for comment in comments_data:
    print(comment)

# 3. 게시글 데이터와 댓글 데이터를 결합합니다.
# 이 예제에서는 단순히 게시글 ID가 1인 게시글과 그에 대한 댓글만 결합합니다.
post_comments = []
for post in posts_data:
    if post['id'] == post_id:
        for comment in comments_data:
            combined = {**post, **comment}  # Merge dictionaries
            post_comments.append(combined)

# 결합된 데이터 출력
print("\nCombined post and comments for post 1:")
for item in post_comments:
    print(item)

# 4. 여러 사용자의 게시글 수 계산하기
# 모든 게시글을 가져옵니다.
url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
all_posts_data = response.json()

# 사용자 ID별로 게시글 수를 계산합니다.
post_counts = {}
for post in all_posts_data:
    user_id = post['userId']
    if user_id in post_counts:
        post_counts[user_id] += 1
    else:
        post_counts[user_id] = 1

# 결과 출력
print("\nPost counts by user:")
for user_id, count in post_counts.items():
    print(f"User {user_id}: {count} posts")
