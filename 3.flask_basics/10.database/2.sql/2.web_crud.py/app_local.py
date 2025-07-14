from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# 메모리 기반 사용자 저장소
users = []    # 예: [{'id': 1, 'name': '홍길동', 'age': 30}, ...]
next_id = 1   # ID 자동 증가

@app.route('/', methods=['GET', 'POST'])
def index():
    global next_id
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])

        # 사용자 추가
        users.append({'id': next_id, 'name': name, 'age': age})
        next_id += 1

        return redirect('/')

    return render_template("index_dict.html", users=users)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return redirect('/')

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return "사용자를 찾을 수 없습니다.", 404

    if request.method == 'POST':
        user['name'] = request.form['name']
        user['age'] = int(request.form['age'])
        return redirect('/')

    return render_template("update_dict.html", user=user)

if __name__ == '__main__':
    app.run(debug=True)
