from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'<User {self.username}, Email {self.email}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}, UserId {self.user_id}>'

@app.route('/')
def index():
    if "user" in session:
        user = User.query.filter_by(username=session["user"]).first()
        posts = Post.query.filter_by(user_id=user.id).all()
        return render_template("index.html", posts=posts)
    return render_template("index.html", posts=None)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        found_user = User.query.filter_by(username=username).first()
        if found_user and found_user.password == password:
            session["user"] = username
            session["email"] = found_user.email
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

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists, please choose another.")
            return redirect(url_for("signin"))

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("signin.html")

@app.route("/view")
def view():
    users = User.query.all()

    users_with_posts = []
    for user in users:
        user_posts = Post.query.filter_by(user_id=user.id).all()
        users_with_posts.append((user, user_posts))

    return render_template("view.html", users_with_posts=users_with_posts)

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            action = request.form["action"]
            if action == "submit":
                email = request.form["email"]
                session["email"] = email
                found_user = User.query.filter_by(username=user).first()
                found_user.email = email
                db.session.commit()
                flash("Email was saved!")
            elif action == "delete":
                found_user = User.query.filter_by(username=user).first()
                db.session.delete(found_user)
                db.session.commit()
                return redirect(url_for("logout"))
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

        # 새로운 게시물 추가
        title = request.form['title']
        content = request.form['content']
        user = User.query.filter_by(username=session["user"]).first()

        new_post = Post(title=title, content=content, user_id=user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_post.html')

@app.route('/del_post/<int:post_id>', methods=['POST'])
def del_post(post_id):
    if "user" not in session:
        flash("You need to log in to delete a post.")
        return redirect(url_for("login"))

    post = Post.query.get_or_404(post_id)
    user = User.query.filter_by(username=session["user"]).first()

    if post.author != user:
        flash("You can only delete your own posts.")
        return redirect(url_for("index"))

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # 기본 사용자 추가 (필요한 경우)
        if not User.query.first():
            user1 = User(username="user1", password="password1", email="user1@example.com")
            user2 = User(username="user2", password="password2", email="user2@example.com")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

    app.run(debug=True, port=5000)
