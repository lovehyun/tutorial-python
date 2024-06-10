from flask import Flask

app = Flask(__name__)

# 경로 매개변수 처리
@app.route('/user/<username>')
def show_user_profile(username):
    # username은 문자열로 전달됩니다
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # post_id는 정수로 전달됩니다
    return f'Post {post_id}'

if __name__ == '__main__':
    app.run(debug=True)
