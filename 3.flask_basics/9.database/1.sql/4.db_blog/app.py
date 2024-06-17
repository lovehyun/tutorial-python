from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

DATABASE = 'app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id))''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    if "user" in session:
        conn = get_db_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM users WHERE username = ?", (session["user"],)).fetchone()
        posts = cur.execute("SELECT * FROM posts WHERE user_id = ?", (user["id"],)).fetchall()
        conn.close()
        return render_template("index.html", posts=posts)
    return render_template("index.html", posts=None)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and user["password"] == password:
            session["user"] = username
            session["email"] = user["email"]
            flash("Login Successful!")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password, please try again.")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("index"))

        return render_template("login.html")

@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = get_db_connection()
        cur = conn.cursor()
        existing_user = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            flash("Username already exists, please choose another.")
            conn.close()
            return redirect(url_for("signin"))

        cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()

        flash("Registration Successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("signin.html")

@app.route("/view")
def view():
    conn = get_db_connection()
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users").fetchall()
    posts = cur.execute("SELECT * FROM posts").fetchall()
    conn.close()

    users_with_posts = []
    for user in users:
        user_posts = [post for post in posts if post["user_id"] == user["id"]]
        users_with_posts.append((user, user_posts))

    return render_template("view.html", users_with_posts=users_with_posts)

@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        username = session["user"]
        
        if request.method == "POST":
            action = request.form["action"]
            conn = get_db_connection()
            cur = conn.cursor()
            if action == "submit":
                email = request.form["email"]
                session["email"] = email
                cur.execute("UPDATE users SET email = ? WHERE username = ?", (email, username))
                conn.commit()
                flash("Email was saved!")
            elif action == "delete":
                cur.execute("DELETE FROM users WHERE username = ?", (username,))
                conn.commit()
                conn.close()
                return redirect(url_for("logout"))
            conn.close()
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        if "user" not in session:
            flash("You need to log in to add a post.")
            return redirect(url_for("login"))

        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM users WHERE username = ?", (session["user"],)).fetchone()

        cur.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)", (title, content, user["id"]))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_post.html')

@app.route('/del_post/<int:post_id>', methods=['POST'])
def del_post(post_id):
    if "user" not in session:
        flash("You need to log in to delete a post.")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()
    post = cur.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    user = cur.execute("SELECT * FROM users WHERE username = ?", (session["user"],)).fetchone()

    if post["user_id"] != user["id"]:
        flash("You can only delete your own posts.")
        conn.close()
        return redirect(url_for("index"))

    cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()
        if not cur.execute("SELECT * FROM users").fetchone():
            cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ("user1", "password1", "user1@example.com"))
            cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ("user2", "password2", "user2@example.com"))
            conn.commit()
        conn.close()

    app.run(debug=True, port=5000)
