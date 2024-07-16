# jsonplaceholder_api.py

import requests

class JSONPlaceholderAPI:
    def __init__(self):
        self.base_url = 'https://jsonplaceholder.typicode.com'

    def get_posts_by_user(self, user_id):
        url = f'{self.base_url}/posts?userId={user_id}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_comments_by_post(self, post_id):
        url = f'{self.base_url}/posts/{post_id}/comments'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def create_post(self, user_id, title, body):
        url = f'{self.base_url}/posts'
        payload = {
            'userId': user_id,
            'title': title,
            'body': body
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def update_post(self, post_id, title=None, body=None):
        url = f'{self.base_url}/posts/{post_id}'
        payload = {}
        if title:
            payload['title'] = title
        if body:
            payload['body'] = body
        response = requests.put(url, json=payload)
        response.raise_for_status()
        return response.json()

    def delete_post(self, post_id):
        url = f'{self.base_url}/posts/{post_id}'
        response = requests.delete(url)
        response.raise_for_status()
        return response.status_code

    def get_all_posts(self):
        url = f'{self.base_url}/posts'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_post_counts_by_user(self):
        all_posts = self.get_all_posts()
        post_counts = {}
        for post in all_posts:
            user_id = post['userId']
            if user_id in post_counts:
                post_counts[user_id] += 1
            else:
                post_counts[user_id] = 1
        return post_counts
