from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')  # form 태그에서 name='username' 값을 받음
    return f'안녕하세요, {username}님!'

if __name__ == '__main__':
    app.run(debug=True)
