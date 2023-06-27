from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    users = [
        {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
        {'name': 'Bob', 'age': 30, 'phone': '987-654-3210'},
        {'name': 'Charlie', 'age': 35, 'phone': '555-123-4567'}
    ]
    
    # 사용자로부터 전달된 GET 매개변수 "name" 가져오기
    user_name = request.args.get('name')
    
    # 사용자 이름이 전달되었을 경우 해당 사용자 정보 필터링
    if user_name:
        users = [user for user in users if user['name'] == user_name]
    
    return render_template('users4.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
