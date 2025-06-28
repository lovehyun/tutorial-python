# ===================================================================
# 파이썬 6단계: 반복문 실습 코드
# ===================================================================

# ===================================================================
# 1. for 반복문 기본 사용법
# ===================================================================

print("=== for 반복문 기초 ===")

# 기본 for 반복문
print("1부터 5까지 출력:")
for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(f"숫자: {i}")

print("\n문자열의 각 글자 출력:")
name = "파이썬"
for char in name:
    print(f"글자: {char}")

print("\n리스트의 각 요소 출력:")
fruits = ["사과", "바나나", "오렌지", "포도"]
for fruit in fruits:
    print(f"과일: {fruit}")

# 인덱스와 함께 출력
print("\n인덱스와 함께 출력:")
for i in range(len(fruits)):
    print(f"{i}번째 과일: {fruits[i]}")

# enumerate() 함수 사용 (더 파이썬다운 방법)
print("\nenumerate() 사용:")
for index, fruit in enumerate(fruits):
    print(f"{index}번째 과일: {fruit}")

# ===================================================================
# 2. range() 함수 활용
# ===================================================================

print("\n=== range() 함수 활용 ===")

# range(stop): 0부터 stop-1까지
print("range(5):")
for i in range(5):
    print(i, end=" ")
print()

# range(start, stop): start부터 stop-1까지
print("\nrange(2, 8):")
for i in range(2, 8):
    print(i, end=" ")
print()

# range(start, stop, step): start부터 stop-1까지 step 간격으로
print("\nrange(0, 10, 2) - 짝수:")
for i in range(0, 10, 2):
    print(i, end=" ")
print()

print("\nrange(10, 0, -1) - 거꾸로:")
for i in range(10, 0, -1):
    print(i, end=" ")
print()

# 실용적인 range 사용 예제
print("\n=== 구구단 3단 ===")
for i in range(1, 10):
    result = 3 * i
    print(f"3 × {i} = {result}")

print("\n=== 1부터 10까지의 합 ===")
total = 0
for i in range(1, 11):
    total += i
    print(f"{i}까지의 합: {total}")

# ===================================================================
# 3. while 반복문 기본 사용법
# ===================================================================

print("\n=== while 반복문 기초 ===")

# 기본 while 반복문
print("1부터 5까지 출력 (while):")
count = 1
while count <= 5:
    print(f"숫자: {count}")
    count += 1

# 조건이 만족될 때까지 반복
print("\n2의 거듭제곱 (1000 이하):")
power = 1
exponent = 0
while power <= 1000:
    print(f"2^{exponent} = {power}")
    exponent += 1
    power = 2 ** exponent

# 사용자 입력 대기 (시뮬레이션)
print("\n비밀번호 입력 시뮬레이션:")
password = "1234"
attempts = 0
max_attempts = 3

# 실제로는 input()을 사용하지만, 예제에서는 시뮬레이션
user_inputs = ["wrong", "123", "1234"]  # 예제용 입력들

for user_input in user_inputs:
    attempts += 1
    print(f"시도 {attempts}: 비밀번호 입력 - '{user_input}'")
    
    if user_input == password:
        print("✅ 로그인 성공!")
        break
    else:
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"❌ 틀렸습니다. {remaining}번 더 시도할 수 있습니다.")
        else:
            print("❌ 로그인 실패! 최대 시도 횟수를 초과했습니다.")
            break

# ===================================================================
# 4. break와 continue
# ===================================================================

print("\n=== break와 continue ===")

# break 예제 - 특정 조건에서 반복 중단
print("1부터 10까지 중 5에서 중단:")
for i in range(1, 11):
    if i == 5:
        print(f"{i}에서 중단!")
        break
    print(i)

# continue 예제 - 특정 조건을 건너뛰기
print("\n1부터 10까지 중 짝수만 출력:")
for i in range(1, 11):
    if i % 2 != 0:  # 홀수면 건너뛰기
        continue
    print(f"짝수: {i}")

# 실용적인 break와 continue 예제
print("\n=== 소수 찾기 (2부터 20까지) ===")
for num in range(2, 21):
    is_prime = True
    
    # 2부터 num-1까지 나누어보기
    for i in range(2, num):
        if num % i == 0:
            is_prime = False
            break  # 나누어 떨어지면 소수가 아니므로 중단
    
    if is_prime:
        print(f"{num}은(는) 소수입니다.")

print("\n=== 양수만 더하기 ===")
numbers = [1, -3, 5, -2, 8, -1, 4, 0, 7]
positive_sum = 0

for num in numbers:
    if num <= 0:
        continue  # 0 이하면 건너뛰기
    positive_sum += num
    print(f"양수 {num} 추가, 현재 합: {positive_sum}")

print(f"양수들의 총합: {positive_sum}")

# ===================================================================
# 5. 중첩 반복문 (Nested Loops)
# ===================================================================

print("\n=== 중첩 반복문 ===")

# 기본 중첩 반복문
print("구구단 2단~9단:")
for dan in range(2, 10):
    print(f"\n{dan}단:")
    for i in range(1, 10):
        result = dan * i
        print(f"{dan} × {i} = {result}")

print("\n=== 별 패턴 만들기 ===")

# 직각삼각형 패턴
print("직각삼각형:")
for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()  # 줄바꿈

# 역직각삼각형 패턴
print("\n역직각삼각형:")
for i in range(5, 0, -1):
    for j in range(i):
        print("*", end="")
    print()

# 정삼각형 패턴
print("\n정삼각형:")
for i in range(1, 6):
    # 공백 출력
    for j in range(5 - i):
        print(" ", end="")
    # 별 출력
    for k in range(2 * i - 1):
        print("*", end="")
    print()

# 다이아몬드 패턴
print("\n다이아몬드:")
# 위쪽 삼각형 (본인 포함)
for i in range(1, 5):
    for j in range(5 - i):
        print(" ", end="")
    for k in range(2 * i - 1):
        print("*", end="")
    print()

# 아래쪽 삼각형
for i in range(3, 0, -1):
    for j in range(5 - i):
        print(" ", end="")
    for k in range(2 * i - 1):
        print("*", end="")
    print()

print("\n=== 좌표계 출력 ===")
# 2차원 좌표 출력
for y in range(3, -1, -1):  # y: 3, 2, 1, 0
    for x in range(4):      # x: 0, 1, 2, 3
        print(f"({x},{y})", end=" ")
    print()

# ===================================================================
# 6. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 숫자 맞추기 게임 ===")

import random

# 컴퓨터가 1~100 사이의 숫자를 선택
secret_number = random.randint(1, 100)
print("1부터 100 사이의 숫자를 맞춰보세요!")

# 게임 시뮬레이션 (실제로는 input() 사용)
user_guesses = [50, 75, 88, 92, 90]  # 예제용 추측들
attempts = 0
max_attempts = 10

for guess in user_guesses:
    attempts += 1
    print(f"\n시도 {attempts}: {guess}")
    
    if guess == secret_number:
        print(f"🎉 정답! {attempts}번 만에 맞췄습니다!")
        break
    elif guess < secret_number:
        print("⬆️ 더 큰 숫자입니다.")
    else:
        print("⬇️ 더 작은 숫자입니다.")
    
    if attempts >= max_attempts:
        print(f"😞 게임 종료! 정답은 {secret_number}이었습니다.")
        break

print(f"정답: {secret_number}")

print("\n=== 실습 예제 2: 점수 입력 및 분석 ===")

# 여러 학생의 점수 입력 및 분석
print("학급 성적 분석 프로그램")

# 실제로는 input()으로 입력받지만, 예제에서는 미리 준비
students_scores = [
    ("김철수", 85),
    ("이영희", 92),
    ("박민수", 78),
    ("최영수", 95),
    ("한지민", 88)
]

total_score = 0
highest_score = 0
lowest_score = 100
highest_student = ""
lowest_student = ""

print("\n성적 입력 결과:")
for name, score in students_scores:
    print(f"{name}: {score}점")
    
    total_score += score
    
    if score > highest_score:
        highest_score = score
        highest_student = name
    
    if score < lowest_score:
        lowest_score = score
        lowest_student = name

average_score = total_score / len(students_scores)

print(f"\n=== 분석 결과 ===")
print(f"총 학생 수: {len(students_scores)}명")
print(f"총점: {total_score}점")
print(f"평균: {average_score:.1f}점")
print(f"최고점: {highest_student} ({highest_score}점)")
print(f"최저점: {lowest_student} ({lowest_score}점)")

# 학점별 분포
grade_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

print(f"\n=== 학점별 분포 ===")
for name, score in students_scores:
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    
    grade_count[grade] += 1
    print(f"{name}: {grade}학점")

print(f"\n학점 통계:")
for grade, count in grade_count.items():
    if count > 0:
        percentage = (count / len(students_scores)) * 100
        print(f"{grade}학점: {count}명 ({percentage:.1f}%)")

print("\n=== 실습 예제 3: 패스워드 생성기 ===")

import random
import string

def generate_password(length=8, include_symbols=True):
    """패스워드 생성 함수"""
    # 사용할 문자들
    lowercase = string.ascii_lowercase  # a-z
    uppercase = string.ascii_uppercase  # A-Z
    digits = string.digits              # 0-9
    symbols = "!@#$%^&*"
    
    # 기본 문자 집합
    characters = lowercase + uppercase + digits
    
    if include_symbols:
        characters += symbols
    
    # 패스워드 생성
    password = ""
    for _ in range(length):
        password += random.choice(characters)
    
    return password

# 여러 종류의 패스워드 생성
print("패스워드 생성기")
print("-" * 30)

password_configs = [
    (8, False, "기본 8자리"),
    (12, True, "특수문자 포함 12자리"),
    (6, False, "간단한 6자리"),
    (16, True, "강력한 16자리")
]

for length, symbols, description in password_configs:
    password = generate_password(length, symbols)
    print(f"{description}: {password}")

print("\n=== 실습 예제 4: 간단한 ATM 시뮬레이터 ===")

# ATM 기능 시뮬레이션
balance = 50000  # 초기 잔액
pin = "1234"     # 비밀번호

print("🏧 ATM 시뮬레이터")
print("=" * 30)

# 로그인 시뮬레이션
login_attempts = ["1111", "1234"]  # 예제용 입력

for attempt_pin in login_attempts:
    print(f"PIN 입력: {attempt_pin}")
    if attempt_pin == pin:
        print("✅ 로그인 성공!")
        break
    else:
        print("❌ 잘못된 PIN입니다.")
else:
    print("로그인 실패로 종료")
    exit()

# ATM 메뉴 시뮬레이션
transactions = [
    (1, 0),      # 잔액 조회
    (2, 10000),  # 입금
    (3, 5000),   # 출금
    (1, 0),      # 잔액 조회
    (4, 0)       # 종료
]

for menu_choice, amount in transactions:
    print(f"\n메뉴 선택: {menu_choice}")
    
    if menu_choice == 1:  # 잔액 조회
        print(f"현재 잔액: {balance:,}원")
    
    elif menu_choice == 2:  # 입금
        print(f"입금액: {amount:,}원")
        if amount > 0:
            balance += amount
            print(f"입금 완료! 현재 잔액: {balance:,}원")
        else:
            print("올바른 금액을 입력해주세요.")
    
    elif menu_choice == 3:  # 출금
        print(f"출금액: {amount:,}원")
        if amount <= 0:
            print("올바른 금액을 입력해주세요.")
        elif amount > balance:
            print("잔액이 부족합니다.")
        else:
            balance -= amount
            print(f"출금 완료! 현재 잔액: {balance:,}원")
    
    elif menu_choice == 4:  # 종료
        print("ATM을 종료합니다. 이용해 주셔서 감사합니다!")
        break
    
    else:
        print("올바른 메뉴를 선택해주세요.")

# ===================================================================
# 7. 반복문과 자료구조 조합
# ===================================================================

print("\n=== 반복문과 리스트 조합 ===")

# 리스트 컴프리헨션 (List Comprehension)
print("1부터 10까지의 제곱수:")
squares = [i**2 for i in range(1, 11)]
print(squares)

print("\n짝수만 필터링:")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = [num for num in numbers if num % 2 == 0]
print(even_numbers)

print("\n문자열 처리:")
words = ["python", "java", "javascript", "c++"]
upper_words = [word.upper() for word in words]
print("원본:", words)
print("대문자:", upper_words)

# 딕셔너리와 반복문
print("\n=== 딕셔너리와 반복문 ===")
student_grades = {
    "김철수": 85,
    "이영희": 92,
    "박민수": 78,
    "최영수": 95
}

print("학생별 성적:")
for name, grade in student_grades.items():
    if grade >= 90:
        level = "우수"
    elif grade >= 80:
        level = "양호"
    else:
        level = "보통"
    print(f"{name}: {grade}점 ({level})")

# 딕셔너리 업데이트
print("\n성적 업데이트 (보너스 점수 +5점):")
for name in student_grades:
    student_grades[name] += 5
    print(f"{name}: {student_grades[name]}점")

# ===================================================================
# 8. 무한 루프와 제어
# ===================================================================

print("\n=== 무한 루프 시뮬레이션 ===")

# while True를 사용한 무한 루프 시뮬레이션
# 실제로는 무한히 실행되지만, 예제에서는 제한된 반복으로 시뮬레이션

counter = 0
max_iterations = 5  # 예제용 제한

print("무한 루프 시뮬레이션 (5번만 실행):")
while True:
    counter += 1
    print(f"반복 {counter}번째")
    
    # 예제용 종료 조건
    if counter >= max_iterations:
        print("예제 종료 조건 도달")
        break
    
    # 실제 프로그램에서는 사용자 입력이나 특정 조건으로 break

print("\n=== 메뉴 시스템 시뮬레이션 ===")

# 메뉴 시스템 예제
menu_choices = [1, 2, 3, 1, 4]  # 예제용 선택들

for choice in menu_choices:
    print(f"\n메뉴 선택: {choice}")
    
    if choice == 1:
        print("📊 데이터 조회")
    elif choice == 2:
        print("✏️ 데이터 입력")
    elif choice == 3:
        print("🗑️ 데이터 삭제")
    elif choice == 4:
        print("👋 프로그램 종료")
        break
    else:
        print("❌ 잘못된 선택입니다.")

print("\n=== 6단계 완료! ===")
print("반복문을 모두 배웠습니다.")
print("다음 단계에서는 데이터 구조(리스트, 딕셔너리 등)를 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
6단계에서 기억해야 할 중요한 점들:

1. for 반복문: 정해진 횟수나 시퀀스에 대해 반복
2. while 반복문: 조건이 참인 동안 계속 반복
3. range() 함수: range(start, stop, step)
4. break: 반복문 완전히 빠져나가기
5. continue: 현재 반복만 건너뛰고 다음 반복 계속
6. 중첩 반복문: 반복문 안에 반복문
7. enumerate(): 인덱스와 값을 함께 얻기
8. 무한 루프: while True (종료 조건 필수)

실습할 때 꼭 해보세요:
- 다양한 패턴 출력하기
- 숫자 게임 만들기
- 메뉴 시스템 구현하기
- 데이터 처리 프로그램 작성하기
- break와 continue 활용하기
"""
