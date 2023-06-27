from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hannah', 'Ivy', 'Jack']
    return render_template('users2.html', names=user_names)

if __name__ == '__main__':
    app.run(debug=True)
