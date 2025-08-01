import hashlib

# 비밀번호 해싱 함수 (SHA-256)
def generate_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return generate_hash(plain_password) == hashed_password

# 테스트용 코드
password = "hello123"

# 1. 해시 생성 (항상 같은 결과)
hashed1 = generate_hash(password)
hashed2 = generate_hash(password)

print("Hashed 1:", hashed1)
print("Hashed 2:", hashed2)
print("같은가?", hashed1 == hashed2)  # 항상 True

# 2. 검증
print("검증 1:", verify_password("hello123", hashed1))  # True
print("검증 2:", verify_password("hello123", hashed2))  # True
print("틀린 비밀번호:", verify_password("wrongpass", hashed1))  # False
