import pandas as pd
import requests

# 특정 사용자 ID를 기준으로 게시글을 가져옵니다.
user_id = 1
url = f'https://jsonplaceholder.typicode.com/posts?userId={user_id}'
response = requests.get(url)
posts_data = response.json()

# 게시글 데이터를 DataFrame으로 변환합니다.
posts_df = pd.DataFrame(posts_data)


# 게시글 ID를 기준으로 첫 번째 게시글의 댓글을 가져옵니다.
post_id = 1
url = f'https://jsonplaceholder.typicode.com/posts/{post_id}/comments'
response = requests.get(url)
comments_data = response.json()

# 댓글 데이터를 DataFrame으로 변환합니다.
comments_df = pd.DataFrame(comments_data)

# 게시글 데이터와 댓글 데이터를 결합합니다.
# 이 예제에서는 단순히 게시글 ID가 1인 게시글과 그에 대한 댓글만 결합합니다.
post_comments_df = pd.merge(posts_df[posts_df['id'] == post_id], comments_df, left_on='id', right_on='postId')

# 결합된 DataFrame 출력
print(post_comments_df)
