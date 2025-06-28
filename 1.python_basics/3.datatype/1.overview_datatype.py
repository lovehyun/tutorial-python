# ===================================================================
# 파이썬 2단계: 기본 데이터 타입과 변수 실습 코드
# ===================================================================

# ===================================================================
# 1. 변수 선언과 할당 (Variable Declaration and Assignment)
# ===================================================================

print("=== 변수 기초 ===")

# 변수 생성 및 값 할당
name = "김파이썬"      # 문자열 변수
age = 25              # 정수 변수
height = 175.5        # 실수 변수
is_student = True     # 불린 변수

# 변수 값 출력
print("이름:", name)
print("나이:", age)
print("키:", height)
print("학생 여부:", is_student)

# 변수 값 변경
print("\n=== 변수 값 변경 ===")
age = 26              # 나이 변경
print("변경된 나이:", age)

is_student = False    # 학생 여부 변경
print("변경된 학생 여부:", is_student)

# 여러 변수에 동시에 값 할당
print("\n=== 여러 변수 동시 할당 ===")
x, y, z = 10, 20, 30
print("x =", x, ", y =", y, ", z =", z)

# 같은 값을 여러 변수에 할당
a = b = c = 100
print("a =", a, ", b =", b, ", c =", c)

# ===================================================================
# 2. 숫자형 (Numbers) - 정수와 실수
# ===================================================================

print("\n=== 정수형 (Integer) ===")

# 정수 변수들
positive_num = 42          # 양의 정수
negative_num = -17         # 음의 정수
zero = 0                   # 0

print("양의 정수:", positive_num)
print("음의 정수:", negative_num)
print("0:", zero)

# 큰 수도 가능 (파이썬은 정수 크기 제한이 거의 없음)
big_number = 123456789012345678901234567890
print("큰 수:", big_number)

print("\n=== 실수형 (Float) ===")

# 실수 변수들
pi = 3.14159               # 일반적인 실수
temperature = -15.5        # 음의 실수
scientific = 1.23e-4       # 과학적 표기법 (0.000123)

print("파이:", pi)
print("온도:", temperature)
print("과학적 표기법:", scientific)

# 실수와 정수의 연산
result = 10 + 3.5
print("정수 + 실수 =", result, "(타입:", type(result), ")")

# ===================================================================
# 3. 문자열 (String) 기본 조작
# ===================================================================

print("\n=== 문자열 기초 ===")

# 문자열 생성 방법들
single_quote = '작은따옴표로 만든 문자열'
double_quote = "큰따옴표로 만든 문자열"
multiline = """여러 줄에 걸친
문자열을 만들 때는
따옴표 3개를 사용합니다"""

print("작은따옴표:", single_quote)
print("큰따옴표:", double_quote)
print("여러 줄 문자열:")
print(multiline)

# 문자열 안에 따옴표 포함하기
quote1 = "그가 말했다: '안녕하세요'"
quote2 = '그녀가 말했다: "반갑습니다"'
quote3 = "그가 말했다: \"안녕하세요\""  # 이스케이프 문자 사용

print(quote1)
print(quote2)
print(quote3)

# 문자열 연결 (Concatenation)
print("\n=== 문자열 연결 ===")
first_name = "파이"
last_name = "썬"
full_name = first_name + last_name
print("이름:", full_name)

greeting = "안녕하세요, " + full_name + "님!"
print(greeting)

# 문자열 반복
print("\n=== 문자열 반복 ===")
laugh = "하" * 5
print("웃음:", laugh)

line = "-" * 20
print(line)

# ===================================================================
# 4. 불린형 (Boolean)
# ===================================================================

print("\n=== 불린형 기초 ===")

# 불린 값들
is_sunny = True
is_raining = False

print("맑은 날씨:", is_sunny)
print("비 오는 날씨:", is_raining)

# 불린 값은 숫자로도 사용 가능
print("True를 숫자로:", int(is_sunny))      # 1
print("False를 숫자로:", int(is_raining))   # 0

# 다른 값들을 불린으로 변환
print("\n=== 다른 타입을 불린으로 ===")
print("1을 불린으로:", bool(1))           # True
print("0을 불린으로:", bool(0))           # False
print("빈 문자열:", bool(""))            # False
print("문자가 있는 문자열:", bool("hello"))  # True

# ===================================================================
# 5. 타입 확인 (Type Checking)
# ===================================================================

print("\n=== 타입 확인하기 ===")

# 다양한 변수들의 타입 확인
number = 42
decimal = 3.14
text = "안녕하세요"
flag = True

print("number의 타입:", type(number))
print("decimal의 타입:", type(decimal))
print("text의 타입:", type(text))
print("flag의 타입:", type(flag))

# 타입을 문자열로 확인
print("number는 int 타입인가?", type(number).__name__ == 'int')

# ===================================================================
# 6. 변수 명명 규칙과 예제
# ===================================================================

print("\n=== 올바른 변수명 예제 ===")

# 올바른 변수명들
user_name = "김파이썬"        # 스네이크 케이스 (권장)
userName = "이자바"          # 카멜 케이스
age2 = 25                   # 숫자 포함 가능 (끝에)
_private = "비공개"          # 언더스코어로 시작 가능

print("사용자명:", user_name)
print("사용자명2:", userName)
print("나이2:", age2)
print("비공개:", _private)

# 잘못된 변수명들 (주석으로만 설명)
# 2age = 25        # 숫자로 시작 불가
# user-name = "김"  # 하이픈 사용 불가
# class = "학생"    # 예약어 사용 불가

# ===================================================================
# 7. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 개인정보 관리 ===")

# 개인정보를 변수로 저장
student_name = "홍길동"
student_id = 20241001
gpa = 3.85
is_graduated = False

print("학생 이름:", student_name)
print("학번:", student_id)
print("학점:", gpa)
print("졸업 여부:", is_graduated)

print("\n=== 실습 예제 2: 상품 정보 ===")

# 상품 정보 변수들
product_name = "노트북"
price = 1500000
discount_rate = 0.15
is_available = True

# 할인된 가격 계산
discounted_price = price * (1 - discount_rate)

print("상품명:", product_name)
print("원가:", price, "원")
print("할인율:", discount_rate * 100, "%")
print("할인가:", discounted_price, "원")
print("재고 있음:", is_available)

print("\n=== 실습 예제 3: 문자열 조작 ===")

# 문자열 변수들
city = "서울"
country = "대한민국"
year = 2025

# 문자열 조합
location = city + ", " + country
message = "저는 " + location + "에 살고 있습니다."
year_message = str(year) + "년입니다."  # 숫자를 문자열로 변환

print("위치:", location)
print("메시지:", message)
print("연도:", year_message)

# ===================================================================
# 8. 타입 변환 (Type Conversion)
# ===================================================================

print("\n=== 타입 변환 예제 ===")

# 문자열을 숫자로
str_number = "123"
int_number = int(str_number)
float_number = float(str_number)

print("문자열:", str_number, "타입:", type(str_number))
print("정수로 변환:", int_number, "타입:", type(int_number))
print("실수로 변환:", float_number, "타입:", type(float_number))

# 숫자를 문자열로
original_number = 456
str_converted = str(original_number)

print("원래 숫자:", original_number, "타입:", type(original_number))
print("문자열로 변환:", str_converted, "타입:", type(str_converted))

# 불린 변환
print("\n=== 불린 변환 ===")
print("int(True):", int(True))
print("int(False):", int(False))
print("str(True):", str(True))
print("str(False):", str(False))

# ===================================================================
# 9. 연습 문제들
# ===================================================================

print("\n=== 연습 문제 ===")

# 연습문제 1: 자기소개 변수 만들기
my_name = "당신의 이름"
my_age = 25
my_hobby = "독서"
my_height = 170.5

print("연습문제 1 - 자기소개:")
print("안녕하세요! 제 이름은", my_name, "입니다.")
print("나이는", my_age, "살이고,")
print("취미는", my_hobby, "입니다.")
print("키는", my_height, "cm입니다.")

# 연습문제 2: 계산기 변수
print("\n연습문제 2 - 간단한 계산:")
num1 = 15
num2 = 7
sum_result = num1 + num2
diff_result = num1 - num2

print(num1, "+", num2, "=", sum_result)
print(num1, "-", num2, "=", diff_result)

# 연습문제 3: 문자열 조합
print("\n연습문제 3 - 문자열 조합:")
adjective = "아름다운"
noun = "날씨"
sentence = "오늘은 " + adjective + " " + noun + "입니다."
print(sentence)

# ===================================================================
# 10. 변수 사용 시 주의사항
# ===================================================================

print("\n=== 주의사항 예제 ===")

# 변수를 선언하기 전에 사용하면 에러 발생
# print(undefined_variable)  # NameError 발생 (주석 처리)

# 대소문자 구분
Name = "김대문자"
name = "김소문자"
print("Name:", Name)
print("name:", name)
print("Name과 name은 다른 변수입니다!")

# 예약어는 변수명으로 사용 불가 (예제로만 설명)
# if = 10      # SyntaxError (주석 처리)
# for = 20     # SyntaxError (주석 처리)

print("\n=== 2단계 완료! ===")
print("변수와 기본 데이터 타입을 배웠습니다.")
print("다음 단계에서는 연산자를 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
2단계에서 기억해야 할 중요한 점들:

1. 변수명은 의미있게 짓기 (name, age보다는 student_name, student_age)
2. 파이썬은 동적 타이핑 언어 (변수 타입을 미리 선언하지 않음)
3. 변수 타입은 할당된 값에 따라 자동으로 결정됨
4. 문자열과 숫자를 더하려면 타입 변환 필요
5. 변수명은 대소문자를 구분함

연습할 때 꼭 해보세요:
- 다양한 타입의 변수 만들어보기
- type() 함수로 타입 확인해보기
- 타입 변환 연습하기
- 의미있는 변수명 짓기 연습
"""
