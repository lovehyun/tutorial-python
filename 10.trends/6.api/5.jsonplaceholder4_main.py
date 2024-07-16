# main.py

from api.jsonplaceholder_api import JSONPlaceholderAPI

# Initialize the API
api = JSONPlaceholderAPI()

# 1. Get posts by user
user_posts = api.get_posts_by_user(user_id=1)
print("Posts by user 1:")
print(user_posts)

# 2. Get comments for the first post
post_comments = api.get_comments_by_post(post_id=1)
print("\nComments for post 1:")
print(post_comments)

# 3. Create a new post
new_post = api.create_post(user_id=1, title="New Post", body="This is a new post.")
print("\nNew post created:")
print(new_post)

# 4. Update an existing post
updated_post = api.update_post(post_id=1, title="Updated Title", body="Updated body content.")
print("\nUpdated post 1:")
print(updated_post)

# 5. Delete a post
delete_status = api.delete_post(post_id=1)
print(f"\nDelete status for post 1: {delete_status}")

# 6. Get post counts by user
post_counts = api.get_post_counts_by_user()
print("\nPost counts by user:")
print(post_counts)
