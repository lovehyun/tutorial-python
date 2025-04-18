import requests

# API 엔드포인트 URL
url = 'https://jsonplaceholder.typicode.com/users'

##########
# GET
##########
post_id = 1
response = requests.get(f"{url}/{post_id}")
print(f"\n[GET] 게시글 ID {post_id} 조회:")
print(response.json())

##########
# POST
##########
new_post = {
    "title": "ChatGPT is awesome",
    "body": "Indeed, it can code too!",
    "userId": 1
}
response = requests.post(url, json=new_post)
print("\n[POST] 게시글 생성:")
print(response.json())

##########
# PUT
##########
post_id = 1
updated_post = {
    "id": post_id,
    "title": "Updated Title",
    "body": "Updated Body",
    "userId": 1
}
response = requests.put(f"{url}/{post_id}", json=updated_post)
print(f"\n[PUT] 게시글 ID {post_id} 수정:")
print(response.json())

##########
# PATCH
##########
patch_data = {
    "title": "Partially Updated Title"
}
response = requests.patch(f"{url}/1", json=patch_data)
print("\n[PATCH] 게시글 일부 수정:")
print(response.json())

##########
# DELETE
##########
response = requests.delete(f"{url}/1")
print("\n[DELETE] 게시글 삭제 상태 코드:")
print(response.status_code)
