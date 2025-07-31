# 1. 회원가입 시
from werkzeug.security import generate_password_hash

pw1 = generate_password_hash("hello123")
pw2 = generate_password_hash("hello123")

print("PW1:", pw1)
print("PW2:", pw2)

print("같은가?", pw1 == pw2)  # False

# PW1: pbkdf2:sha256:260000$Ahv7...$QOcv...
# PW2: pbkdf2:sha256:260000$Hkdo...$3DP0...
# 같은가? False

# 똑같은 hello123 인데 해시값이 다름 (랜덤 솔트 때문)


# 2. 로그인 시 비교
from werkzeug.security import check_password_hash

is_valid = check_password_hash(pw1, "hello123")  # True

print("비교1:", check_password_hash(pw1, "hello123"))  # True
print("비교2:", check_password_hash(pw2, "hello123"))  # True
# 비교1: True
# 비교2: True


# 내부적으로 무슨 일이 벌어지나?
# 1. 비밀번호 해시 (generate_password_hash) 생성 시:
#  - pbkdf2:sha256:260000$<salt>$<hashed> 형태로 저장됨
#  - 이 안에:
#     - 어떤 알고리즘을 썼는지
#     - 몇 번 반복했는지
#     - 어떤 솔트를 썼는지가 포함되어 있음
# 2. 비교 함수 (check_password_hash)는:
#  - 이 정보를 분석해서
#  - 같은 조건으로 입력한 비밀번호를 다시 해싱
#  - 그 결과와 비교하여 일치 여부만 판단

# 왜 이렇게 반복을 많이 하나요? (600,000회?)
# ✔ 이유는 브루트포스 공격 방지
