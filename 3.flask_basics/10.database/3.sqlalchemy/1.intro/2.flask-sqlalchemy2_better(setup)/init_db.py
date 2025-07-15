from app import create_app  # 방법2 로 한 경우
# from app import app  # 방법1 로 한 경우

from models import db, User


app = create_app()  # 방법2 로 한 경우

# A. 모두다 초기화 후 새로 셋업
with app.app_context():
    db.drop_all()      # 모든 테이블 삭제
    db.create_all()    # 다시 생성

    # 새 데이터 삽입
    db.session.add(User(name="Alice", age=30))
    db.session.add(User(name="Bob", age=20))
    db.session.commit()

    for user in User.query.all():
        print(user.name, user.age)


# B. 데이터 없으면 초기화, 있으면 그대로 두기
# with app.app_context():
#     db.create_all()    # 테이블 생성
#
#     # 중복 삽입 방지
#     if not User.query.first():
#         db.session.add(User(name="Alice", age=30))
#         db.session.add(User(name="Bob", age=20))
#         db.session.commit()
#
#     # 확인용 출력
#     for user in User.query.all():
#         print(user.name, user.age)
