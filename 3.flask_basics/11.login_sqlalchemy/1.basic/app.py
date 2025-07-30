from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# 이 Flask 코드는 **사용자 인증 시스템(회원가입, 로그인, 로그아웃, 프로필 수정)**이 포함된 간단한 웹 애플리케이션입니다

"""
LoginManager: 로그인 관리를 담당하는 클래스로, Flask 애플리케이션에서 로그인 기능을 초기화하고 관리하는 역할을 합니다.
UserMixin: UserMixin 클래스는 Flask-Login이 기본적으로 사용하는 사용자 모델 클래스를 정의하기 위해 사용됩니다. 이 클래스를 사용하여 사용자 모델 클래스에 필요한 메서드들을 간단하게 추가할 수 있습니다.
login_user: 로그인 처리를 위해 사용되는 함수로, 인증이 성공적으로 완료된 사용자를 로그인 상태로 만듭니다. 이 함수를 호출하면 세션에 사용자 정보가 저장되어 사용자를 인증된 상태로 유지할 수 있습니다.
login_required: 데코레이터로, 특정 뷰 함수를 보호하는 데 사용됩니다. 이 데코레이터가 적용된 뷰 함수는 로그인된 사용자만 접근할 수 있으며, 로그인되지 않은 사용자는 로그인 페이지로 리디렉션됩니다.
logout_user: 로그아웃 처리를 위해 사용되는 함수로, 현재 로그인된 사용자를 로그아웃 상태로 만듭니다. 세션에서 사용자 정보를 삭제하여 인증을 끝내는 역할을 합니다.
current_user: 현재 로그인된 사용자를 나타내는 객체입니다. 로그인되지 않은 경우 AnonymousUserMixin 객체가 반환됩니다. 이를 통해 로그인된 사용자의 정보를 뷰 함수에서 간단하게 접근할 수 있습니다.
"""

app = Flask(__name__)

# Flask 애플리케이션 설정
app.config['SECRET_KEY'] = 'your-secret-key'  # 세션 데이터 암호화에 사용되는 비밀 키 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite 데이터베이스 URI 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy 이벤트 시스템 비활성화

# SQLAlchemy 및 Flask-Login 초기화
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 로그인 페이지를 지정

# 사용자 모델 정의
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 사용자 ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # 사용자 이름, 고유 및 필수
    password = db.Column(db.String(120), nullable=False)  # 비밀번호

    # 비밀번호 설정 메서드
    def set_password(self, password):
        self.password = password

    # 비밀번호 확인 메서드
    def check_password(self, password):
        return self.password == password

# 사용자 로더 콜백 함수
@login_manager.user_loader
def load_user(user_id):
    # 현재 애플리케이션 컨텍스트에서 사용자 로드
    with current_app.app_context():
        return db.session.get(User, int(user_id))

@app.route('/')
def main():
    return render_template('main.html')  # 메인 페이지 렌더링

# 로그인된 사용자만 접근 가능한 페이지
@app.route('/users')
@login_required
def view_users():
    users = User.query.all()  # 모든 사용자 조회
    return render_template('users.html', users=users)  # 사용자 목록 페이지 렌더링

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()  # 사용자 조회

        if user and user.check_password(password):
            login_user(user)  # 사용자 로그인
            return redirect(url_for('main'))  # 메인 페이지로 리디렉션
        else:
            return "아이디나 비밀번호가 잘못되었습니다."  # 오류 메시지

    return redirect(url_for('main'))  # 로그인 페이지 렌더링

# 로그아웃 처리
@app.route('/logout')
@login_required
def logout():
    logout_user()  # 사용자 로그아웃
    return redirect(url_for('main'))  # 메인 페이지로 리디렉션

# 사용자 프로필 수정 페이지
@app.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        new_password = request.form['new_password']

        current_user.set_password(new_password)  # 비밀번호 변경
        db.session.commit()  # 변경 사항 저장

        return redirect(url_for('main'))  # 메인 페이지로 리디렉션

    return render_template('profile_edit.html', current_user=current_user)  # 프로필 수정 페이지 렌더링

# 회원가입 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()  # 사용자 조회
        if existing_user:
            return "이미 사용 중인 아이디입니다."  # 오류 메시지

        new_user = User(username=username)
        new_user.set_password(password)  # 비밀번호 설정
        db.session.add(new_user)  # 새로운 사용자 추가
        db.session.commit()  # 변경 사항 저장

        return redirect(url_for('main'))  # 메인 페이지로 리디렉션

    return render_template('register.html')  # 회원가입 페이지 렌더링

# 애플리케이션 실행
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 데이터베이스 테이블 생성
    app.run(debug=True)  # 디버그 모드로 애플리케이션 실행
