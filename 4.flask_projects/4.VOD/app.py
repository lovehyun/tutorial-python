from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'

# Sample user data
users = {
    "user@example.com": generate_password_hash("password")
}

# Sample video data
videos = [
    {'id': 1, 'title': 'Sample Video', 'filename': 'sample_video.mp4'},
]

@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', videos=videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and check_password_hash(users[email], password):
            session['email'] = email
            return redirect(url_for('index'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            return "User already exists"
        users[email] = generate_password_hash(password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/video/<int:video_id>')
def video(video_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    video = next((v for v in videos if v['id'] == video_id), None)
    if video:
        return render_template('video.html', video=video)
    else:
        return "Video not found"

@app.route('/stream/<filename>')
def stream(filename):
    return send_file(f'videos/{filename}')

if __name__ == '__main__':
    app.run(debug=True)
