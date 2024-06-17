# 여기서는 SQLAlchemy의 주요 구성 요소들을 임포트하고 있습니다:
# - create_engine: 데이터베이스 연결을 생성하는 함수.
# - Column, Integer, String: 데이터베이스 테이블의 컬럼을 정의하는 데 사용되는 클래스들.
# - declarative_base: 모델 클래스의 베이스 클래스를 생성하는 함수.
# - sessionmaker: 데이터베이스 세션을 생성하는 함수.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
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
