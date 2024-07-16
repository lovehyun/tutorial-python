import requests

class JSONPlaceholderAPI:
    def __init__(self):
        self.base_url = 'https://jsonplaceholder.typicode.com'
        self.cache = {}

    def _get_cache_key(self, endpoint, params=None):
        if params:
            param_str = '&'.join(f"{key}={value}" for key, value in sorted(params.items()))
            return f"{endpoint}?{param_str}"
        return endpoint

    def _get(self, endpoint, params=None):
        cache_key = self._get_cache_key(endpoint, params)
        if cache_key in self.cache:
            print(f"*** Fetching from cache - Key: {cache_key} ***")
            return self.cache[cache_key]
        print(f"*** Fetching from API - Key: {cache_key} ***")
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        self.cache[cache_key] = data
        print(f"*** Caching data - Key: {cache_key} ***")
        return data

    def _invalidate_cache(self, cache_key):
        if cache_key in self.cache:
            print(f"*** Invalidating cache for key: {cache_key} ***")
            self.cache.pop(cache_key)

    # GET method, Endpoint URL: https://jsonplaceholder.typicode.com/posts?userId={user_id}
    def get_posts_by_user(self, user_id):
        return self._get('posts', {'userId': user_id})

    # GET method, Endpoint URL: https://jsonplaceholder.typicode.com/posts/{post_id}/comments
    def get_comments_by_post(self, post_id):
        return self._get(f'posts/{post_id}/comments')

    # POST method, Endpoint URL: https://jsonplaceholder.typicode.com/posts
    def create_post(self, user_id, title, body):
        url = f'{self.base_url}/posts'
        payload = {
            'userId': user_id,
            'title': title,
            'body': body
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        # Invalidate cache for the posts list
        self._invalidate_cache(self._get_cache_key('posts', {'userId': user_id}))
        return response.json()

    # PUT method, Endpoint URL: https://jsonplaceholder.typicode.com/posts/{post_id}
    def update_post(self, post_id, title=None, body=None):
        url = f'{self.base_url}/posts/{post_id}'
        payload = {}
        if title:
            payload['title'] = title
        if body:
            payload['body'] = body
        response = requests.put(url, json=payload)
        response.raise_for_status()
        # Invalidate cache for this post and related lists
        self._invalidate_cache(self._get_cache_key(f'posts/{post_id}'))
        return response.json()

    # DELETE method, Endpoint URL: https://jsonplaceholder.typicode.com/posts/{post_id}
    def delete_post(self, post_id):
        url = f'{self.base_url}/posts/{post_id}'
        response = requests.delete(url)
        response.raise_for_status()
        # Invalidate cache for this post and related lists
        self._invalidate_cache(self._get_cache_key(f'posts/{post_id}'))
        return response.status_code

    # GET method, Endpoint URL: https://jsonplaceholder.typicode.com/posts
    def get_all_posts(self):
        return self._get('posts')

    # GET method, Endpoint URL: https://jsonplaceholder.typicode.com/posts
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

    def view_cache(self):
        # return self.cache
        print("\n--- Cache Start ---")
        for key, value in self.cache.items():
            print(f"Key: {key}, Value: {value}")
        print("--- Cache End ---\n")
