# SQLAlchemy를 사용한 Flask 데이터베이스 모델 및 쿼리

## 1. 데이터베이스 모델 정의
SQLAlchemy를 사용하여 데이터베이스 테이블을 나타내는 클래스를 정의할 수 있습니다. 모델 클래스는 db.Model을 상속받고, 각 속성은 db.Column을 사용하여 정의합니다.

### User 모델
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
```

## 2. 데이터베이스 쿼리

### 레코드 추가
```python
new_user = User(username="john_doe", password="secret", email="john_doe@example.com")
db.session.add(new_user)
db.session.commit()
```

### 레코드 조회
- 모든 레코드 조회
```python
users = User.query.all()
```

- 단일 레코드 조회
```python
user = User.query.get(1)  # ID가 1인 사용자 조회
```

- 조건부 조회
```python
user = User.query.filter_by(username="john_doe").first()
```

### 레코드 업데이트
```python
user = User.query.filter_by(username="john_doe").first()
if user:
    user.email = "new_email@example.com"
    db.session.commit()
```

### 레코드 삭제
```python
user = User.query.filter_by(username="john_doe").first()
if user:
    db.session.delete(user)
    db.session.commit()
```

## 3. 관계 정의
SQLAlchemy를 사용하여 모델 간의 관계를 정의할 수 있습니다. 예를 들어, User 모델과 Post 모델 간의 일대다 관계를 정의할 수 있습니다.

### 관계 설정
- User 모델에 posts 관계 정의
```python
posts = db.relationship('Post', backref='author', lazy=True)
```

- Post 모델에 외래 키 설정
```python
user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### 관계를 통해 데이터 조회
- 사용자로부터 게시물 조회
```python
user = User.query.filter_by(username="john_doe").first()
user_posts = user.posts  # User 모델의 posts 관계를 통해 게시물 조회
```

## 4. 고급 쿼리

### 필터와 정렬
- 여러 조건으로 필터링
```python
users = User.query.filter(User.username.like('%john%'), User.email.endswith('@example.com')).all()
```

- 정렬
```python
users = User.query.order_by(User.username.desc()).all()
```

### 리미트와 오프셋
- 상위 10명의 사용자 조회
```python
users = User.query.limit(10).all()
```

- 10번째 이후의 사용자 조회
```python
users = User.query.offset(10).all()
```

## 5. 세션 관리
SQLAlchemy의 세션은 데이터베이스 작업을 관리하는 컨텍스트입니다. 일반적인 세션 관리 예제는 다음과 같습니다.

### 세션 시작 및 커밋
```python
db.session.add(new_user)
db.session.commit()
```

### 세션 롤백
```python
try:
    db.session.add(new_user)
    db.session.commit()
except:
    db.session.rollback()
```
