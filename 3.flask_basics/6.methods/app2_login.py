from flask import Flask, render_template, request

app = Flask(__name__)

# 사용자 목록
users = [
    {'name': 'Alice', 'id': 'alice', 'pw': 'alice'},
    {'name': 'Bob', 'id': 'bob', 'pw': 'bob1234'},
    {'name': 'Charlie', 'id': 'charlie', 'pw': 'hello'},
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # POST 방식의 FORM-Data 에서 id와 password 가져오기
        id = request.form['id']
        pw = request.form['password']

        # 사용자 목록과 매칭 확인
        # user = None
        # for u in users:
        #     if u['id'] == id and u['pw'] == pw:
        #         user = u
        #         break
        user = next((user for user in users if user['id'] == id and user['pw'] == pw), None)

        if user:
            error = None
        else:
            error = "Invalid ID or password"

        return render_template('index2.html', user=user, error=error)

    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)
