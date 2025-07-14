# pip install sqlalchemy

# 여기서는 SQLAlchemy의 주요 구성 요소들을 임포트하고 있습니다:
# - create_engine: 데이터베이스 연결을 생성하는 함수.
# - Column, Integer, String: 데이터베이스 테이블의 컬럼을 정의하는 데 사용되는 클래스들.
# - declarative_base: 모델 클래스의 베이스 클래스를 생성하는 함수.
# - sessionmaker: 데이터베이스 세션을 생성하는 함수.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 엔진 생성 (SQLite 사용)
# - create_engine: SQLite 데이터베이스 파일 example.db와 연결된 엔진 객체를 생성합니다.
# - 'sqlite:///example.db': SQLite 데이터베이스 파일의 경로를 지정하는 URI입니다.
engine = create_engine('sqlite:///example.db')

# 베이스 클래스 생성
# - SQLAlchemy의 ORM 시스템에서 사용할 베이스 클래스를 생성합니다. 
# - 모든 모델 클래스는 이 베이스 클래스를 상속받아야 합니다. 
# - 이 베이스 클래스는 메타데이터를 포함하여, 데이터베이스 테이블과 클래스 간의 매핑을 관리합니다.
Base = declarative_base()

# 사용자 모델 정의
# - __tablename__: 데이터베이스에서 사용할 테이블 이름을 지정합니다.
# - id, name, age: 테이블의 컬럼을 정의합니다.
# - id: 기본 키로 설정된 정수형 컬럼.
# - name: 문자열형 컬럼.
# - age: 정수형 컬럼.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# 데이터베이스 테이블 생성
# - Base.metadata.create_all(engine): 베이스 클래스에 정의된 모든 테이블을 실제 데이터베이스에 생성합니다. 
# - 여기서는 User 클래스에 해당하는 users 테이블을 생성합니다.
Base.metadata.create_all(engine)

# 세션 생성
# - sessionmaker(bind=engine): 엔진과 연결된 세션 팩토리를 생성합니다.
# - session = Session(): 세션 팩토리에서 세션 객체를 생성합니다. 이 세션 객체는 데이터베이스와의 상호작용을 관리합니다.
Session = sessionmaker(bind=engine)
session = Session()

# 새로운 사용자 추가
# - new_user = User(name='John Doe', age=30): User 모델의 인스턴스를 생성합니다.
# - session.add(new_user): 새 사용자 객체를 세션에 추가합니다.
# - session.commit(): 세션의 변경사항을 커밋하여, 데이터베이스에 실제로 반영합니다.
new_user = User(name='John Doe', age=30)
session.add(new_user)
session.commit()

# 모든 사용자 조회
# - session.query(User).all(): User 테이블의 모든 레코드를 조회하여 리스트로 반환합니다.
# - for user in users: 사용자 리스트를 순회하면서 각 사용자의 name과 age를 출력합니다.
users = session.query(User).all()
for user in users:
    print(user.name, user.age)

# CRUD 헬퍼 함수 예시 ----------------------------------------------

def create_user(session, name: str, age: int) -> User:
    """사용자 추가(생성)"""
    new_user = User(name=name, age=age)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)            # INSERT 후 갱신된 PK 값 가져오기
    return new_user

def get_user_by_id(session, user_id: int) -> User | None:
    """ID로 사용자 조회(단건 READ)"""
    return session.get(User, user_id)    # SQLAlchemy 2.x 스타일의 편리한 get

def list_users(session) -> list[User]:
    """모든 사용자 조회(다건 READ)"""
    return session.query(User).all()

def update_user_age(session, user_id: int, new_age: int) -> bool:
    """사용자 나이 수정(UPDATE) – 성공 시 True"""
    user = session.get(User, user_id)
    if not user:
        return False
    user.age = new_age
    session.commit()
    return True

def delete_user(session, user_id: int) -> bool:
    """사용자 삭제(DELETE) – 성공 시 True"""
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

# ---------------------------------------------------------------

if __name__ == "__main__":
    # 세션 준비
    # SQLAlchemy ORM에서는 세션(Session)이 꼭 필요합니다.
    # ORM은 단순한 SQL 실행기가 아니라, 객체(클래스)와 DB 레코드 간의 상태를 동기화하고, 이를 추적·관리하는 시스템이기 때문입니다.
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    
    with Session() as session:
        # 1) CREATE
        john = create_user(session, "John Doe", 30)
        jane = create_user(session, "Jane Doe", 28)
        print(f"추가된 사용자 ID: {john.id}, {jane.id}")

        # 2) READ (단건·다건)
        user = get_user_by_id(session, john.id)
        print(f"단건 조회: {user.name}, {user.age}")

        print("전체 사용자 목록:")
        for u in list_users(session):
            print(f"   • {u.id}: {u.name}({u.age})")

        # 3) UPDATE
        updated = update_user_age(session, jane.id, 29)
        print(f"Jane 나이 수정 성공? {updated}")

        # 4) DELETE
        deleted = delete_user(session, john.id)
        print(f"John 삭제 성공? {deleted}")

        print("최종 사용자 목록:")
        for u in list_users(session):
            print(f"   • {u.id}: {u.name}({u.age})")
