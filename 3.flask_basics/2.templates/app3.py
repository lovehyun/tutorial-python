from flask import Flask, render_template

app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'name': 'Bob', 'age': 30, 'phone': '987-654-3210'},
    {'name': 'Charlie', 'age': 35, 'phone': '555-123-4567'}
]

@app.route('/')
def index():
    return render_template('users3.html', users=users)

@app.route('/user/<name>')
def get_user_by_name(name):
    # 이름이 일치하는 사용자 필터링
    user = None
    for u in users:
        if u['name'].lower() == name.lower():
            user = u
            break

    # 위 5줄을 간결한 한줄짜리 코드로 변경 - next() 함수 사용
    # user = next((user for user in users if user['name'].lower() == name.lower()), None)
    
    if user:
        return render_template('users3.html', users=[user])
    else:
        return render_template('users3.html', users=[])

if __name__ == '__main__':
    app.run(debug=True)
