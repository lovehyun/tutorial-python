from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'id': 2, 'name': 'Alice', 'age': 30, 'phone': '123-654-9870'},
    {'id': 3, 'name': 'Bob', 'age': 30, 'phone': '987-654-3210'},
    {'id': 4, 'name': 'Charlie', 'age': 35, 'phone': '555-123-4567'}
]

@app.route('/')
def index():
    name_query = request.args.get('name')
    age_query = request.args.get('age')
    phone_query = request.args.get('phone')

    filtered_users = users

    if name_query:
        filtered_users = [user for user in filtered_users if name_query.lower() in user['name'].lower()]
    
    if age_query:
        try:
            filtered_users = [user for user in filtered_users if int(age_query) == user['age']]
        except ValueError:
            # 나이가 정수로 변환되지 않으면 빈 리스트 반환
            filtered_users = []

    if phone_query:
        filtered_users = [user for user in filtered_users if phone_query in user['phone']]
        
    return render_template('users5.html', users=filtered_users)

if __name__ == '__main__':
    app.run(debug=True)
