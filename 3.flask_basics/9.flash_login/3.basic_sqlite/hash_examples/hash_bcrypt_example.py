# pip install bcrypt
import bcrypt

# 비밀번호 해싱 함수
def generate_hash(password: str) -> bytes:
    salt = bcrypt.gensalt()  # 솔트 자동 생성
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


# 테스트용 코드
password = "hello123"

# 1. 해시 생성 (매번 다른 결과)
hashed1 = generate_hash(password)
hashed2 = generate_hash(password)

print("Hashed 1:", hashed1.decode())
print("Hashed 2:", hashed2.decode())
print("같은가?", hashed1 == hashed2)  # False

# 2. 검증
print("검증 1:", verify_password("hello123", hashed1))  # True
print("검증 2:", verify_password("hello123", hashed2))  # True
print("틀린 비밀번호:", verify_password("wrongpass", hashed1))  # False
