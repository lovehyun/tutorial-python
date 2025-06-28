# ===================================================================
# 파이썬 4단계: 입출력 실습 코드
# ===================================================================

# ===================================================================
# 1. print() 함수 기본 사용법
# ===================================================================

print("=== print() 함수 기본 ===")

# 기본 출력
print("안녕하세요!")
print("파이썬을 배우고 있습니다.")

# 여러 값을 한 번에 출력
print("이름:", "김파이썬", "나이:", 25)

# 변수 출력
name = "홍길동"
age = 30
print("이름:", name, "나이:", age)

# 다양한 데이터 타입 출력
number = 42
decimal = 3.14159
boolean = True
print("정수:", number, "실수:", decimal, "불린:", boolean)

print("\n=== print() 함수 고급 옵션 ===")

# sep 매개변수 - 구분자 변경
print("사과", "바나나", "오렌지")  # 기본 구분자는 공백
print("사과", "바나나", "오렌지", sep=", ")  # 쉼표로 구분
print("2025", "12", "25", sep="-")  # 하이픈으로 구분
print("A", "B", "C", sep="")  # 구분자 없음

# end 매개변수 - 끝 문자 변경
print("첫 번째 줄", end="")  # 줄바꿈 없음
print("같은 줄에 출력")

print("Hello", end=" ")
print("World", end="!\n")

print("Loading", end="")
for i in range(5):
    print(".", end="")
print(" 완료!")

# 여러 매개변수 조합
print("\n=== 매개변수 조합 ===")
print("년", "월", "일", sep="-", end=" ")
print("시", "분", "초", sep=":", end="\n")

# ===================================================================
# 2. input() 함수 기본 사용법
# ===================================================================

print("\n=== input() 함수 기본 ===")

# 기본 입력 받기 (실제 실행 시에는 사용자가 입력해야 함)
# 주석으로 예제를 보여드리고, 실제 값을 할당하여 진행하겠습니다.

# user_name = input("이름을 입력하세요: ")
user_name = "김파이썬"  # 예제용 값
print("안녕하세요,", user_name, "님!")

# user_age = input("나이를 입력하세요: ")
user_age = "25"  # 예제용 값 (문자열로 받아짐)
print("입력받은 나이:", user_age)
print("나이의 타입:", type(user_age))  # str 타입임을 확인

print("\n=== input()으로 받은 값 처리 ===")

# 문자열을 숫자로 변환
# str_number = input("숫자를 입력하세요: ")
str_number = "42"  # 예제용
number = int(str_number)
print("입력받은 숫자:", number)
print("숫자 + 10 =", number + 10)

# 실수 입력 받기
# str_decimal = input("소수를 입력하세요: ")
str_decimal = "3.14"  # 예제용
decimal = float(str_decimal)
print("입력받은 소수:", decimal)
print("소수 * 2 =", decimal * 2)

# 한 번에 변환하기
# age = int(input("나이를 입력하세요: "))
age = int("25")  # 예제용
print("입력받은 나이:", age)
print("내년 나이:", age + 1)

# ===================================================================
# 3. 문자열 포매팅 (String Formatting)
# ===================================================================

print("\n=== 문자열 포매팅 기본 ===")

# % 포매팅 (옛날 방식)
name = "김파이썬"
age = 25
print("이름: %s, 나이: %d" % (name, age))

# .format() 메서드
print("이름: {}, 나이: {}".format(name, age))
print("이름: {0}, 나이: {1}".format(name, age))
print("나이: {1}, 이름: {0}".format(name, age))  # 순서 바꾸기

# 변수명 지정
print("이름: {name}, 나이: {age}".format(name=name, age=age))

print("\n=== f-string (추천 방식) ===")

# f-string - 파이썬 3.6+ (가장 간단하고 직관적)
name = "이파이썬"
age = 30
height = 175.5

print(f"이름: {name}")
print(f"나이: {age}")
print(f"키: {height}cm")

# 계산식도 가능
print(f"내년 나이: {age + 1}")
print(f"키(미터): {height / 100}m")

# 다양한 표현
price = 12500
print(f"가격: {price}원")
print(f"가격: {price:,}원")  # 천 단위 쉼표
print(f"가격: {price:>10}원")  # 오른쪽 정렬 (10자리)
print(f"가격: {price:<10}원")  # 왼쪽 정렬
print(f"가격: {price:^10}원")  # 가운데 정렬

# 소수점 자리수 조정
pi = 3.141592653589793
print(f"파이: {pi}")
print(f"파이 (소수점 2자리): {pi:.2f}")
print(f"파이 (소수점 4자리): {pi:.4f}")

print("\n=== 고급 f-string 사용법 ===")

# 퍼센트 표시
score = 0.856
print(f"점수: {score:.1%}")  # 85.6%

# 날짜와 시간 (예제)
year = 2025
month = 6
day = 28
print(f"오늘 날짜: {year}-{month:02d}-{day:02d}")  # 02d는 2자리 0 패딩

# 변수명과 값 동시 출력 (파이썬 3.8+)
temperature = 25.7
humidity = 60
print(f"{temperature=}")  # temperature=25.7
print(f"{humidity=}")     # humidity=60

# ===================================================================
# 4. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 간단한 계산기 ===")

# 사용자로부터 두 숫자를 입력받아 계산
# 실제로는 input()을 사용하지만, 예제에서는 값을 직접 할당
# num1 = float(input("첫 번째 숫자를 입력하세요: "))
# num2 = float(input("두 번째 숫자를 입력하세요: "))

num1 = 15.5  # 예제용
num2 = 4.2   # 예제용

print(f"입력된 숫자: {num1}, {num2}")
print(f"덧셈: {num1} + {num2} = {num1 + num2}")
print(f"뺄셈: {num1} - {num2} = {num1 - num2}")
print(f"곱셈: {num1} × {num2} = {num1 * num2}")
print(f"나눗셈: {num1} ÷ {num2} = {num1 / num2:.2f}")

print("\n=== 실습 예제 2: 개인정보 입력 프로그램 ===")

# 여러 정보를 입력받아 정리된 형태로 출력
# name = input("이름: ")
# age = int(input("나이: "))
# city = input("거주 도시: ")
# hobby = input("취미: ")

# 예제용 데이터
name = "박파이썬"
age = 28
city = "서울"
hobby = "프로그래밍"

print("\n" + "="*30)
print("개인정보 요약")
print("="*30)
print(f"이름: {name}")
print(f"나이: {age}세")
print(f"거주지: {city}")
print(f"취미: {hobby}")
print(f"내년 나이: {age + 1}세")
print("="*30)

print("\n=== 실습 예제 3: 온라인 쇼핑몰 주문 ===")

# 상품 정보 입력
# product_name = input("상품명: ")
# price = int(input("가격: "))
# quantity = int(input("수량: "))

# 예제용 데이터
product_name = "무선 이어폰"
price = 89000
quantity = 2

# 계산
subtotal = price * quantity
tax = subtotal * 0.1  # 10% 세금
shipping = 3000 if subtotal < 50000 else 0  # 5만원 미만 배송비
total = subtotal + tax + shipping

# 결과 출력
print("\n" + "="*40)
print("주문 내역")
print("="*40)
print(f"상품명: {product_name}")
print(f"단가: {price:,}원")
print(f"수량: {quantity}개")
print("-"*40)
print(f"소계: {subtotal:,}원")
print(f"세금: {tax:,.0f}원")
print(f"배송비: {shipping:,}원")
print("-"*40)
print(f"총 금액: {total:,.0f}원")
print("="*40)

print("\n=== 실습 예제 4: 성적 관리 프로그램 ===")

# 과목별 점수 입력
# korean = int(input("국어 점수: "))
# english = int(input("영어 점수: "))
# math = int(input("수학 점수: "))

# 예제용 데이터
korean = 85
english = 92
math = 78

# 계산
total_score = korean + english + math
average = total_score / 3
grade = "A" if average >= 90 else "B" if average >= 80 else "C" if average >= 70 else "D" if average >= 60 else "F"

# 결과 출력
print("\n" + "="*25)
print("성적표")
print("="*25)
print(f"국어: {korean:>3}점")
print(f"영어: {english:>3}점")
print(f"수학: {math:>3}점")
print("-"*25)
print(f"총점: {total_score:>3}점")
print(f"평균: {average:>5.1f}점")
print(f"학점: {grade:>5}")
print("="*25)

# ===================================================================
# 5. 입력 유효성 검사 기초
# ===================================================================

print("\n=== 입력 유효성 검사 예제 ===")

# 숫자 입력 검사 (예외 처리는 나중에 배우므로 기본적인 방법만)
def is_number(s):
    """문자열이 숫자인지 확인하는 함수"""
    try:
        float(s)
        return True
    except:
        return False

# 예제 테스트
test_inputs = ["123", "45.6", "abc", "12.34.56", "-15"]
for test in test_inputs:
    result = is_number(test)
    print(f"'{test}'는 숫자인가? {result}")

print("\n=== 실습 예제 5: 나이 계산기 ===")

# birth_year = input("태어난 연도를 입력하세요 (예: 1995): ")
birth_year = "1995"  # 예제용

if birth_year.isdigit():  # 숫자인지 확인
    birth_year = int(birth_year)
    current_year = 2025
    age = current_year - birth_year
    
    print(f"\n태어난 연도: {birth_year}년")
    print(f"현재 연도: {current_year}년")
    print(f"현재 나이: {age}세")
    
    # 추가 정보
    if age >= 20:
        print("성인입니다.")
    else:
        print(f"성인까지 {20 - age}년 남았습니다.")
        
    if age >= 65:
        print("경로우대 대상입니다.")
else:
    print("올바른 연도를 입력해주세요.")

# ===================================================================
# 6. 다양한 출력 스타일
# ===================================================================

print("\n=== 다양한 출력 스타일 ===")

# 표 형태로 출력
print("이름      나이  도시")
print("-" * 20)
print(f"{'김철수':<8} {25:>3}  {'서울'}")
print(f"{'이영희':<8} {30:>3}  {'부산'}")
print(f"{'박민수':<8} {28:>3}  {'대구'}")

# 진행률 표시 (간단한 버전)
print("\n다운로드 진행률:")
for i in range(0, 101, 20):
    bar = "█" * (i // 5) + "░" * (20 - i // 5)
    print(f"[{bar}] {i:3}%", end="\r" if i < 100 else "\n")

# 박스 형태 출력
message = "파이썬 학습 중"
width = len(message) + 4
print("┌" + "─" * (width - 2) + "┐")
print(f"│ {message} │")
print("└" + "─" * (width - 2) + "┘")

# ===================================================================
# 7. 연습 문제들
# ===================================================================

print("\n=== 연습 문제 ===")

print("연습문제 1: BMI 계산기")
# height = float(input("키를 입력하세요 (cm): "))
# weight = float(input("몸무게를 입력하세요 (kg): "))

# 예제용 데이터
height = 175  # cm
weight = 70   # kg

height_m = height / 100  # 미터로 변환
bmi = weight / (height_m ** 2)

print(f"키: {height}cm")
print(f"몸무게: {weight}kg")
print(f"BMI: {bmi:.1f}")

if bmi < 18.5:
    category = "저체중"
elif bmi < 25:
    category = "정상"
elif bmi < 30:
    category = "과체중"
else:
    category = "비만"

print(f"분류: {category}")

print("\n연습문제 2: 단위 변환기")
# meters = float(input("미터를 입력하세요: "))
meters = 1000  # 예제용

km = meters / 1000
cm = meters * 100
mm = meters * 1000
inch = meters * 39.37
feet = meters * 3.281

print(f"{meters}미터는...")
print(f"  {km}km")
print(f"  {cm}cm") 
print(f"  {mm}mm")
print(f"  {inch:.2f}인치")
print(f"  {feet:.2f}피트")

print("\n연습문제 3: 시간 변환기")
# total_minutes = int(input("총 분을 입력하세요: "))
total_minutes = 150  # 예제용 (2시간 30분)

hours = total_minutes // 60
minutes = total_minutes % 60

print(f"{total_minutes}분은 {hours}시간 {minutes}분입니다.")

print("\n=== 4단계 완료! ===")
print("입출력과 문자열 포매팅을 배웠습니다.")
print("다음 단계에서는 조건문을 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
4단계에서 기억해야 할 중요한 점들:

1. print() 함수: sep, end 매개변수 활용
2. input() 함수: 항상 문자열을 반환 (타입 변환 필요)
3. f-string: 가장 현대적이고 직관적인 포매팅 방법
4. 포매팅 옵션: :,d (천단위), :.2f (소수점), :>10 (정렬)
5. 입력 검증: isdigit(), isnumeric() 등 활용

실습할 때 꼭 해보세요:
- 다양한 input() 프로그램 만들어보기
- f-string으로 예쁜 출력 만들어보기  
- 계산기, 변환기 등 실용적인 프로그램 작성
- 표 형태나 박스 형태로 출력해보기
- 입력값 검증하는 방법 연습하기
"""
