from flask import Flask, render_template, request, redirect, url_for, flash
from models import get_all_users, add_user, delete_user, get_user, update_user, init_db, initialize_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

@app.route('/')
def index():
    users = get_all_users()
    return render_template('index3.html', users=users)

@app.route('/add', methods=['POST'])
def add_user_route():
    name = request.form.get('name')
    age = request.form.get('age')
    if not name or not age:
        flash('Please enter both name and age')
        return redirect(url_for('index'))
    
    add_user(name, age)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user_route(id):
    delete_user(id)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit_user_route(id):
    user = get_user(id)
    if not user:
        return redirect(url_for('index'))
    return render_template('edit3.html', user=user)

@app.route('/update/<int:id>', methods=['POST'])
def update_user_route(id):
    name = request.form.get('name')
    age = request.form.get('age')
    if not name or not age:
        flash('Please enter both name and age')
        return redirect(url_for('edit_user_route', id=id))

    update_user(id, name, age)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        initialize_database()
        users = get_all_users()
        if not users:
            print('사용자 초기화...')
            add_user('user1', 30)
            add_user('user2', 22)

    app.run(debug=True)
