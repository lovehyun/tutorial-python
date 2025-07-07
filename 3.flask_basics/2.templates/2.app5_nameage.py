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

    filtered_users = users

    if name_query:
        filtered_users = [user for user in filtered_users if name_query.lower() in user['name'].lower()]
    
    if age_query:
        try:
            age_query = int(age_query)
            filtered_users = [user for user in filtered_users if age_query == user['age']]
        except ValueError:
            # 나이가 정수로 변환되지 않으면 빈 리스트 반환
            filtered_users = []

    return render_template('users5.html', users=filtered_users)

# @app.route('/')
# def index():
#     name_query = request.args.get('name')
#     age_query = request.args.get('age')

#     filtered_users = []

#     # 이름과 나이 모두 입력한 경우
#     if name_query and age_query:
#         try:
#             age_query = int(age_query)
#             for user in users:
#                 if name_query.lower() in user['name'].lower() and user['age'] == age_query:
#                     filtered_users.append(user)
#         except ValueError:
#             # 나이가 정수가 아니면 빈 리스트 유지
#             filtered_users = []

#     # 이름만 입력한 경우
#     elif name_query:
#         for user in users:
#             if name_query.lower() in user['name'].lower():
#                 filtered_users.append(user)

#     # 나이만 입력한 경우
#     elif age_query:
#         try:
#             age_query = int(age_query)
#             for user in users:
#                 if user['age'] == age_query:
#                     filtered_users.append(user)
#         except ValueError:
#             filtered_users = []

#     # 둘 다 입력 안 한 경우: 모든 유저 출력
#     else:
#         filtered_users = users

#     return render_template('users5.html', users=filtered_users)

if __name__ == '__main__':
    app.run(debug=True)
