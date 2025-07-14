from flask import Flask, request, redirect, render_template
import db_sqlite as db

app = Flask(__name__)

db.create_table()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        db.insert_user(name, age)
        return redirect('/')

    users = db.get_users()
    return render_template("index_dict.html", users=users)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    db.delete_user(user_id)
    return redirect('/')

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        db.update_user(user_id, name, age)
        return redirect('/')

    user = db.get_user_by_id(user_id)
    return render_template("update_dict.html", user=user)

if __name__ == '__main__':
    app.run(debug=True)
