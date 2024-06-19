from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import sqlite3


app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

DATABASE = 'users.sqlite3'

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
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL)''')
        conn.commit()

        # 기본 사용자 추가 (필요한 경우)
        cur.execute("SELECT COUNT(*) as count FROM users")
        count = cur.fetchone()["count"]
        if count == 0:
            cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ("user1", "password1", "user1@example.com"))
            cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ("user2", "password2", "user2@example.com"))
            conn.commit()
        conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        found_user = cur.fetchone()
        conn.close()

        if found_user and found_user["password"] == password:
            session["user"] = username
            session["email"] = found_user["email"]
            flash("Login Successful!")
            return redirect(url_for("user"))
        else:
            flash("Invalid username or password, please try again.")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash("Username already exists, please choose another.")
            conn.close()
            return redirect(url_for("signin"))

        cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (username, password, email))
        conn.commit()
        conn.close()

        flash("Registration Successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("signin.html")

@app.route("/view")
def view():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template("view.html", users=users)

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            action = request.form["action"]
            conn = get_db_connection()
            cur = conn.cursor()
            
            if action == "submit":
                email = request.form["email"]
                password = request.form["password"]

                if email:
                    session["email"] = email
                    cur.execute("UPDATE users SET email = ? WHERE username = ?", (email, user))
                if password:
                    cur.execute("UPDATE users SET password = ? WHERE username = ?", (password, user))
                
                conn.commit()
                flash("Account details were saved!")
            elif action == "delete":
                cur.execute("DELETE FROM users WHERE username = ?", (user,))
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

# @app.route("/user/delete", methods=["DELETE"])
# def delete_user():
#     if "user" in session:
#         user = session["user"]
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("DELETE FROM users WHERE username = ?", (user,))
#         conn.commit()
#         conn.close()
#         session.pop("user", None)
#         session.pop("email", None)
#         flash("Your account has been deleted.")
#         return '', 204
#     else:
#         flash("You are not logged in!")
#         return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
