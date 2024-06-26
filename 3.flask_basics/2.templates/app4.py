from flask import Flask, render_template, request

app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'name': 'Bob', 'age': 30, 'phone': '987-654-3210'},
    {'name': 'Charlie', 'age': 35, 'phone': '555-123-4567'}
]

@app.route('/')
def index():    
    # 사용자로부터 전달된 GET 매개변수 "name" 가져오기
    user_name = request.args.get('name')
    filtered_users = users
    
    # 사용자 이름이 전달되었을 경우 해당 사용자 정보 필터링
    if user_name:
        filtered_users = [user for user in users if user['name'].lower() == user_name.lower()]
    
    return render_template('users4.html', users=filtered_users)

if __name__ == '__main__':
    app.run(debug=True)
