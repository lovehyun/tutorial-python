# ===================================================================
# 파이썬 3단계: 기본 연산자 실습 코드
# ===================================================================

# ===================================================================
# 1. 산술 연산자 (Arithmetic Operators)
# ===================================================================

print("=== 산술 연산자 기초 ===")

# 기본 변수 설정
a = 15
b = 4

print("a =", a, ", b =", b)
print()

# 덧셈 (+)
addition = a + b
print("덧셈: a + b =", addition)

# 뺄셈 (-)
subtraction = a - b
print("뺄셈: a - b =", subtraction)

# 곱셈 (*)
multiplication = a * b
print("곱셈: a * b =", multiplication)

# 나눗셈 (/) - 결과는 항상 실수
division = a / b
print("나눗셈: a / b =", division)

# 정수 나눗셈 (//) - 소수점 버림
floor_division = a // b
print("정수 나눗셈: a // b =", floor_division)

# 나머지 (%)
remainder = a % b
print("나머지: a % b =", remainder)

# 거듭제곱 (**)
power = a ** b
print("거듭제곱: a ** b =", power)

print("\n=== 음수와 양수 연산 ===")

# 음수와 양수
positive = +10
negative = -10
print("양수:", positive)
print("음수:", negative)

# 음수 연산
x = 8
print("x =", x)
print("-x =", -x)
print("x는 여전히:", x)  # 원래 값은 변하지 않음

print("\n=== 실수 연산 예제 ===")

# 실수 연산
price = 19.99
quantity = 3
tax_rate = 0.08

subtotal = price * quantity
tax = subtotal * tax_rate
total = subtotal + tax

print("가격:", price, "원")
print("수량:", quantity, "개")
print("소계:", subtotal, "원")
print("세금:", tax, "원")
print("총액:", total, "원")

# ===================================================================
# 2. 비교 연산자 (Comparison Operators)
# ===================================================================

print("\n=== 비교 연산자 ===")

# 변수 설정
num1 = 10
num2 = 20
num3 = 10

print("num1 =", num1, ", num2 =", num2, ", num3 =", num3)
print()

# 같음 (==)
print("num1 == num2:", num1 == num2)  # False
print("num1 == num3:", num1 == num3)  # True

# 같지 않음 (!=)
print("num1 != num2:", num1 != num2)  # True
print("num1 != num3:", num1 != num3)  # False

# 크다 (>)
print("num1 > num2:", num1 > num2)    # False
print("num2 > num1:", num2 > num1)    # True

# 작다 (<)
print("num1 < num2:", num1 < num2)    # True
print("num2 < num1:", num2 < num1)    # False

# 크거나 같다 (>=)
print("num1 >= num3:", num1 >= num3)  # True
print("num1 >= num2:", num1 >= num2)  # False

# 작거나 같다 (<=)
print("num1 <= num3:", num1 <= num3)  # True
print("num2 <= num1:", num2 <= num1)  # False

print("\n=== 문자열 비교 ===")

# 문자열 비교 (사전식 순서)
name1 = "apple"
name2 = "banana"
name3 = "apple"

print("name1 =", name1, ", name2 =", name2, ", name3 =", name3)
print("name1 == name3:", name1 == name3)  # True
print("name1 < name2:", name1 < name2)    # True (사전 순서)
print("name2 > name1:", name2 > name1)    # True

# 대소문자 구분
upper_name = "APPLE"
lower_name = "apple"
print("APPLE == apple:", upper_name == lower_name)  # False

# ===================================================================
# 3. 논리 연산자 (Logical Operators)
# ===================================================================

print("\n=== 논리 연산자 ===")

# 불린 변수들
is_sunny = True
is_warm = True
is_raining = False

print("is_sunny =", is_sunny)
print("is_warm =", is_warm)
print("is_raining =", is_raining)
print()

# and 연산자 - 모든 조건이 True일 때만 True
print("=== AND 연산자 ===")
print("is_sunny and is_warm:", is_sunny and is_warm)      # True
print("is_sunny and is_raining:", is_sunny and is_raining)  # False
print("is_warm and is_raining:", is_warm and is_raining)    # False

# or 연산자 - 하나라도 True이면 True
print("\n=== OR 연산자 ===")
print("is_sunny or is_raining:", is_sunny or is_raining)    # True
print("is_warm or is_raining:", is_warm or is_raining)      # True
print("is_raining or False:", is_raining or False)          # False

# not 연산자 - 반대 값
print("\n=== NOT 연산자 ===")
print("not is_sunny:", not is_sunny)      # False
print("not is_raining:", not is_raining)  # True

# 복합 논리 연산
print("\n=== 복합 논리 연산 ===")
good_weather = is_sunny and is_warm and not is_raining
print("좋은 날씨 (맑고 따뜻하고 비 안 옴):", good_weather)

picnic_weather = (is_sunny or is_warm) and not is_raining
print("소풍 가능한 날씨:", picnic_weather)

print("\n=== 숫자와 논리 연산 ===")

# 숫자를 불린으로 사용
age = 20
score = 85

# 비교 연산의 결과를 논리 연산으로 조합
is_adult = age >= 18
is_pass = score >= 60

print("나이:", age, "점수:", score)
print("성인인가?", is_adult)
print("합격인가?", is_pass)
print("성인이면서 합격?", is_adult and is_pass)
print("성인이거나 합격?", is_adult or is_pass)

# ===================================================================
# 4. 할당 연산자 (Assignment Operators)
# ===================================================================

print("\n=== 할당 연산자 ===")

# 기본 할당
count = 10
print("초기 count:", count)

# 덧셈 할당 (+=)
count += 5    # count = count + 5와 같음
print("count += 5 후:", count)

# 뺄셈 할당 (-=)
count -= 3    # count = count - 3과 같음
print("count -= 3 후:", count)

# 곱셈 할당 (*=)
count *= 2    # count = count * 2와 같음
print("count *= 2 후:", count)

# 나눗셈 할당 (/=)
count /= 4    # count = count / 4와 같음
print("count /= 4 후:", count)

# 정수 나눗셈 할당 (//=)
num = 17
print("\n초기 num:", num)
num //= 3     # num = num // 3과 같음
print("num //= 3 후:", num)

# 나머지 할당 (%=)
num %= 4      # num = num % 4와 같음
print("num %= 4 후:", num)

# 거듭제곱 할당 (**=)
base = 3
print("\n초기 base:", base)
base **= 2    # base = base ** 2와 같음
print("base **= 2 후:", base)

# ===================================================================
# 5. 연산자 우선순위 (Operator Precedence)
# ===================================================================

print("\n=== 연산자 우선순위 ===")

# 기본적인 우선순위
result1 = 2 + 3 * 4        # 곱셈이 먼저: 2 + 12 = 14
result2 = (2 + 3) * 4      # 괄호가 먼저: 5 * 4 = 20

print("2 + 3 * 4 =", result1)
print("(2 + 3) * 4 =", result2)

# 복잡한 연산
result3 = 10 + 2 * 3 ** 2  # 거듭제곱 → 곱셈 → 덧셈: 10 + 2 * 9 = 10 + 18 = 28
result4 = (10 + 2) * 3 ** 2  # 괄호 → 거듭제곱 → 곱셈: 12 * 9 = 108

print("10 + 2 * 3 ** 2 =", result3)
print("(10 + 2) * 3 ** 2 =", result4)

# 논리 연산자와 비교 연산자
x = 5
y = 10
result5 = x < y and y > 0   # 비교 먼저, 그 다음 논리: True and True = True
print("x < y and y > 0 =", result5)

# ===================================================================
# 6. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 성적 계산기 ===")

# 과목별 점수
korean = 85
english = 92
math = 78
science = 88

# 총점과 평균
total_score = korean + english + math + science
average = total_score / 4

print("국어:", korean, "영어:", english, "수학:", math, "과학:", science)
print("총점:", total_score)
print("평균:", average)

# 학점 계산 (90 이상 A, 80 이상 B, 70 이상 C, 60 이상 D, 나머지 F)
is_A = average >= 90
is_B = average >= 80 and average < 90
is_C = average >= 70 and average < 80

print("A학점인가?", is_A)
print("B학점인가?", is_B)
print("C학점인가?", is_C)

print("\n=== 실습 예제 2: 온라인 쇼핑몰 ===")

# 상품 정보
item_price = 29000
quantity = 3
shipping_fee = 3000
free_shipping_limit = 50000

# 계산
subtotal = item_price * quantity
is_free_shipping = subtotal >= free_shipping_limit
total_shipping = 0 if is_free_shipping else shipping_fee
total_price = subtotal + total_shipping

print("상품 가격:", item_price, "원")
print("수량:", quantity, "개")
print("소계:", subtotal, "원")
print("무료 배송 조건 (5만원 이상):", is_free_shipping)
print("배송비:", total_shipping, "원")
print("최종 금액:", total_price, "원")

print("\n=== 실습 예제 3: 시간 계산 ===")

# 시간을 초 단위로 저장
total_seconds = 3725  # 1시간 2분 5초

# 시, 분, 초로 변환
hours = total_seconds // 3600
remaining_seconds = total_seconds % 3600
minutes = remaining_seconds // 60
seconds = remaining_seconds % 60

print("총 초:", total_seconds)
print("시간:", hours, "시", minutes, "분", seconds, "초")

print("\n=== 실습 예제 4: 짝수/홀수 판별 ===")

# 여러 숫자들의 짝수/홀수 판별
numbers = [15, 22, 37, 44, 51]

for num in numbers:
    is_even = num % 2 == 0
    is_odd = num % 2 == 1  # 또는 not is_even
    print(f"{num}은(는) 짝수: {is_even}, 홀수: {is_odd}")

# ===================================================================
# 7. 문자열과 연산자
# ===================================================================

print("\n=== 문자열과 연산자 ===")

# 문자열 연결
first_name = "김"
last_name = "파이썬"
full_name = first_name + last_name
print("이름:", full_name)

# 문자열 반복
greeting = "안녕" * 3
print("인사:", greeting)

separator = "-" * 20
print(separator)

# 문자열 비교
password = "python123"
user_input = "python123"
is_correct = password == user_input
print("비밀번호가 맞나요?", is_correct)

# 문자열 포함 확인 (in 연산자)
text = "파이썬 프로그래밍"
has_python = "파이썬" in text
has_java = "자바" in text
print("'파이썬'이 포함되어 있나요?", has_python)
print("'자바'가 포함되어 있나요?", has_java)

# ===================================================================
# 8. 연습 문제들
# ===================================================================

print("\n=== 연습 문제 ===")

# 연습문제 1: 온도 변환기
print("연습문제 1: 섭씨를 화씨로 변환")
celsius = 25
fahrenheit = celsius * 9 / 5 + 32
print(f"섭씨 {celsius}도는 화씨 {fahrenheit}도입니다.")

# 연습문제 2: 할인 계산기
print("\n연습문제 2: 할인 계산")
original_price = 100000
discount_rate = 0.2  # 20% 할인
discount_amount = original_price * discount_rate
final_price = original_price - discount_amount

print(f"원가: {original_price}원")
print(f"할인률: {discount_rate * 100}%")
print(f"할인금액: {discount_amount}원")
print(f"최종가격: {final_price}원")

# 연습문제 3: 나이 계산기
print("\n연습문제 3: 나이 계산")
current_year = 2025
birth_year = 1995
age = current_year - birth_year
is_adult = age >= 18
can_vote = age >= 19  # 한국 선거권 나이

print(f"태어난 해: {birth_year}년")
print(f"현재 연도: {current_year}년")
print(f"나이: {age}살")
print(f"성인인가요? {is_adult}")
print(f"투표할 수 있나요? {can_vote}")

# 연습문제 4: 윤년 판별 (간단 버전)
print("\n연습문제 4: 윤년 판별")
year = 2024
is_leap_year = year % 4 == 0  # 간단한 버전 (실제로는 더 복잡)
print(f"{year}년은 윤년인가요? {is_leap_year}")

# ===================================================================
# 9. 유용한 팁과 트릭
# ===================================================================

print("\n=== 유용한 팁들 ===")

# 변수 값 교환 (파이썬만의 특별한 방법)
a = 10
b = 20
print(f"교환 전: a = {a}, b = {b}")

a, b = b, a  # 파이썬의 독특한 방법
print(f"교환 후: a = {a}, b = {b}")

# 여러 값 동시 비교
score = 85
is_good_score = 80 <= score <= 90  # 80 이상 90 이하
print(f"점수 {score}는 80~90 사이인가요? {is_good_score}")

# 불린 값을 숫자로 활용
correct_answers = 7
total_questions = 10
is_pass = correct_answers >= 6

# True는 1, False는 0으로 계산됨
bonus_points = is_pass * 5  # 합격하면 5점 보너스
final_score = correct_answers + bonus_points

print(f"맞춘 문제: {correct_answers}개")
print(f"합격 여부: {is_pass}")
print(f"보너스 점수: {bonus_points}점")
print(f"최종 점수: {final_score}점")

print("\n=== 3단계 완료! ===")
print("기본 연산자를 모두 배웠습니다.")
print("다음 단계에서는 입출력을 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
3단계에서 기억해야 할 중요한 점들:

1. 산술 연산자: +, -, *, /, //, %, **
2. 비교 연산자: ==, !=, >, <, >=, <=
3. 논리 연산자: and, or, not
4. 할당 연산자: +=, -=, *=, /=, //=, %=, **=
5. 연산자 우선순위: 괄호 > 거듭제곱 > 곱셈,나눗셈 > 덧셈,뺄셈 > 비교 > 논리

실습할 때 꼭 해보세요:
- 다양한 숫자로 산술 연산 해보기
- 문자열과 숫자 비교해보기
- 복잡한 논리 조건 만들어보기
- 할당 연산자로 값 변경해보기
- 연산자 우선순위 실험해보기
"""
