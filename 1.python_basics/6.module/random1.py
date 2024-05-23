# Random 모듈 활용
import random

# 1. 1~100사이의 랜덤 숫자 생성
print("랜덤 숫자:", random.randint(1, 100))


# 2. 주사위 던지기
def roll_dice():
    return random.randint(1, 6)
print("주사위 던지기 결과:", roll_dice())


# 3. 리스트에서 랜덤으로 요소 선택
def choose_random_element(elements):
    random_index = random.randint(0, len(elements) - 1)  # 0부터 length-1 사이의 랜덤한 인덱스 생성
    return elements[random_index]
        
def choose_random_element(elements):
    return random.choice(elements)

elements = ['apple', 'banana', 'cherry', 'grape', 'pineapple']
print("랜덤 선택된 요소:", choose_random_element(elements))


# 4. 리스트 요소 무작위로 섞기
my_list = [1, 2, 3, 4, 5]
def shuffle_list(elements):
    random.shuffle(elements) # shuffle 은 반환값이 없음
    return elements

print("원본 리스트: ", my_list)
print("섞인 리스트: ", shuffle_list(my_list))


# 5. 랜덤으로 문자열 생성 (영문 대문자 6자리)
import string

def generate_random_string(length=6):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

print("랜덤 문자열:", generate_random_string())


# 6. 가중치를 고려한 랜덤
def weighted_random_choice(elements, weights):
    return random.choices(elements, weights=weights, k=1)[0]

elements = ['apple', 'banana', 'cherry']
weights = [0.1, 0.3, 0.6]
print("가중치에 따른 랜덤 선택:", weighted_random_choice(elements, weights))


# 7. 랜덤 비밀번호 생성 (대소문자, 숫자 포함 8자리)
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

print("랜덤 비밀번호:", generate_random_password())


# 8. 강력한 비밀번호 생성기 (3가지 조건 필수 포함)
def generate_strong_password(length=8):
    if length < 3:
        raise ValueError("비밀번호 길이는 최소 3자 이상이어야 합니다.")
    
    # 각 조건을 만족하는 문자 하나씩을 선택
    password = [
        random.choice(string.ascii_uppercase),  # 대문자
        random.choice(string.ascii_lowercase),  # 소문자
        random.choice(string.digits)            # 숫자
    ]
    
    # 남은 길이를 랜덤한 문자로 채우기
    if length > 3:
        characters = string.ascii_letters + string.digits
        password.extend(random.choice(characters) for _ in range(length - 3))
    
    # 비밀번호를 섞어 랜덤성을 높임
    random.shuffle(password)
    
    return ''.join(password)

print("강력한 랜덤 비밀번호:", generate_strong_password())
