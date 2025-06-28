# ===================================================================
# 파이썬 5단계: 조건문 실습 코드
# ===================================================================

# ===================================================================
# 1. if문 기본 사용법
# ===================================================================

print("=== if문 기초 ===")

# 기본 if문
age = 20
if age >= 18:
    print("성인입니다.")
    print("투표할 수 있습니다.")

print("프로그램이 계속 실행됩니다.")

# 조건이 거짓인 경우
age = 15
if age >= 18:
    print("이 메시지는 출력되지 않습니다.")
    
print("나이가 15세이므로 if문 내부가 실행되지 않았습니다.")

# 다양한 조건들
print("\n=== 다양한 조건 예제 ===")

# 숫자 비교
score = 85
if score >= 90:
    print("A학점")

if score >= 80:
    print("우수한 성적입니다!")

# 문자열 비교
name = "김파이썬"
if name == "김파이썬":
    print("반갑습니다, 김파이썬님!")

# 불린 값 직접 사용
is_student = True
if is_student:
    print("학생 할인이 적용됩니다.")

# 논리 연산자와 함께
temperature = 25
humidity = 60
if temperature >= 20 and humidity <= 70:
    print("날씨가 좋습니다!")

# ===================================================================
# 2. if-else문
# ===================================================================

print("\n=== if-else문 ===")

# 기본 if-else
age = 17
if age >= 18:
    print("성인입니다.")
else:
    print("미성년자입니다.")

# 점수에 따른 합격/불합격
score = 75
if score >= 60:
    print("합격입니다!")
else:
    print("불합격입니다.")

# 홀수/짝수 판별
number = 7
if number % 2 == 0:
    print(f"{number}는 짝수입니다.")
else:
    print(f"{number}는 홀수입니다.")

# 양수/음수/0 판별
num = -5
if num > 0:
    print("양수입니다.")
else:
    if num < 0:
        print("음수입니다.")
    else:
        print("0입니다.")

# ===================================================================
# 3. if-elif-else문
# ===================================================================

print("\n=== if-elif-else문 ===")

# 학점 계산
score = 88
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

print(f"점수: {score}, 학점: {grade}")

# 계절 판별
month = 7
if month in [12, 1, 2]:
    season = "겨울"
elif month in [3, 4, 5]:
    season = "봄"
elif month in [6, 7, 8]:
    season = "여름"
elif month in [9, 10, 11]:
    season = "가을"
else:
    season = "잘못된 월"

print(f"{month}월은 {season}입니다.")

# BMI 지수 판별
height = 175  # cm
weight = 70   # kg
bmi = weight / ((height / 100) ** 2)

if bmi < 18.5:
    category = "저체중"
elif bmi < 25:
    category = "정상"
elif bmi < 30:
    category = "과체중"
else:
    category = "비만"

print(f"BMI: {bmi:.1f}, 분류: {category}")

# 여러 조건을 가진 elif
age = 25
income = 3000  # 만원 단위

if age < 18:
    tax_rate = 0
elif age < 65 and income < 2000:
    tax_rate = 0.1
elif age < 65 and income < 5000:
    tax_rate = 0.2
elif age >= 65:
    tax_rate = 0.05
else:
    tax_rate = 0.3

print(f"나이: {age}, 소득: {income}만원, 세율: {tax_rate*100}%")

# ===================================================================
# 4. 중첩 조건문 (Nested if statements)
# ===================================================================

print("\n=== 중첩 조건문 ===")

# 학생 할인 시스템
age = 16
is_student = True

if age < 18:
    print("미성년자입니다.")
    if is_student:
        print("학생 할인 50% 적용")
        discount = 0.5
    else:
        print("일반 미성년자 할인 20% 적용")
        discount = 0.2
else:
    print("성인입니다.")
    if is_student:
        print("성인 학생 할인 30% 적용")
        discount = 0.3
    else:
        print("일반 성인 요금")
        discount = 0

original_price = 10000
final_price = original_price * (1 - discount)
print(f"원가: {original_price}원, 최종가격: {final_price}원")

# 영화 관람 등급 시스템
age = 17
has_guardian = True

if age >= 18:
    print("모든 영화를 관람할 수 있습니다.")
else:
    if age >= 15:
        print("15세 이상 관람가 영화를 볼 수 있습니다.")
        if has_guardian:
            print("보호자 동반 시 청소년 관람불가 영화도 가능합니다.")
    elif age >= 12:
        print("12세 이상 관람가 영화를 볼 수 있습니다.")
    else:
        print("전체 관람가 영화만 볼 수 있습니다.")

# 로그인 시스템
username = "admin"
password = "1234"
is_admin = username == "admin"

if username and password:  # 둘 다 입력되었는지 확인
    if username == "admin" and password == "1234":
        print("관리자로 로그인 되었습니다.")
        if is_admin:
            print("모든 기능에 접근할 수 있습니다.")
    elif username == "user" and password == "user123":
        print("일반 사용자로 로그인 되었습니다.")
        print("제한된 기능만 사용할 수 있습니다.")
    else:
        print("아이디 또는 비밀번호가 틀렸습니다.")
else:
    print("아이디와 비밀번호를 모두 입력해주세요.")

# ===================================================================
# 5. 조건문과 논리 연산자 조합
# ===================================================================

print("\n=== 논리 연산자 조합 ===")

# 장학금 선발 조건
grade_point = 3.8
attendance = 95
volunteer_hours = 30

# 여러 조건을 만족해야 하는 경우 (and)
if grade_point >= 3.5 and attendance >= 90 and volunteer_hours >= 20:
    print("장학금 대상자입니다!")
    
    # 추가 혜택 판별
    if grade_point >= 4.0 and volunteer_hours >= 50:
        scholarship = "전액 장학금"
    elif grade_point >= 3.8 or volunteer_hours >= 40:
        scholarship = "반액 장학금"
    else:
        scholarship = "부분 장학금"
    
    print(f"지급 장학금: {scholarship}")
else:
    print("장학금 대상자가 아닙니다.")
    
    # 어떤 조건이 부족한지 확인
    if grade_point < 3.5:
        print("학점이 부족합니다.")
    if attendance < 90:
        print("출석률이 부족합니다.")
    if volunteer_hours < 20:
        print("봉사시간이 부족합니다.")

# 아르바이트 지원 자격
age = 19
has_experience = False
can_work_night = True

# 복잡한 조건 조합
if age >= 18:
    if has_experience or can_work_night:
        print("아르바이트 지원 가능합니다.")
        
        if has_experience and can_work_night:
            hourly_wage = 12000
            print("경험자 + 야간근무 가능: 시급 12,000원")
        elif has_experience:
            hourly_wage = 10000
            print("경험자: 시급 10,000원")
        elif can_work_night:
            hourly_wage = 9500
            print("야간근무 가능: 시급 9,500원")
    else:
        hourly_wage = 9000
        print("일반: 시급 9,000원")
else:
    print("만 18세 이상만 지원 가능합니다.")

# ===================================================================
# 6. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 온라인 쇼핑몰 배송비 계산 ===")

order_amount = 45000  # 주문 금액
is_member = True      # 회원 여부
region = "서울"       # 배송 지역

print(f"주문 금액: {order_amount:,}원")
print(f"회원 여부: {'회원' if is_member else '비회원'}")
print(f"배송 지역: {region}")

# 배송비 계산 로직
if order_amount >= 50000:
    shipping_fee = 0
    print("무료배송 적용 (5만원 이상)")
elif is_member:
    if region in ["서울", "경기", "인천"]:
        shipping_fee = 2000
        print("회원 할인 배송비 (수도권)")
    else:
        shipping_fee = 3000
        print("회원 할인 배송비 (지방)")
else:
    if region in ["서울", "경기", "인천"]:
        shipping_fee = 3000
        print("일반 배송비 (수도권)")
    else:
        shipping_fee = 4000
        print("일반 배송비 (지방)")

total_amount = order_amount + shipping_fee
print(f"배송비: {shipping_fee:,}원")
print(f"총 결제금액: {total_amount:,}원")

print("\n=== 실습 예제 2: 시험 성적 분석 프로그램 ===")

korean = 88
english = 92
math = 85
science = 90

total = korean + english + math + science
average = total / 4

print("=== 성적표 ===")
print(f"국어: {korean}")
print(f"영어: {english}")
print(f"수학: {math}")
print(f"과학: {science}")
print(f"총점: {total}")
print(f"평균: {average:.1f}")

# 학점 계산
if average >= 95:
    grade = "A+"
elif average >= 90:
    grade = "A"
elif average >= 85:
    grade = "B+"
elif average >= 80:
    grade = "B"
elif average >= 75:
    grade = "C+"
elif average >= 70:
    grade = "C"
elif average >= 65:
    grade = "D+"
elif average >= 60:
    grade = "D"
else:
    grade = "F"

print(f"학점: {grade}")

# 특별 상 계산
if average >= 95:
    award = "최우수상"
elif average >= 90 and all(score >= 85 for score in [korean, english, math, science]):
    award = "우수상"
elif math >= 95 or science >= 95:
    award = "수학/과학 우수상"
else:
    award = "없음"

print(f"수상: {award}")

# 과목별 분석
print("\n=== 과목별 분석 ===")
subjects = {"국어": korean, "영어": english, "수학": math, "과학": science}

for subject, score in subjects.items():
    if score >= 90:
        level = "우수"
    elif score >= 80:
        level = "양호"
    elif score >= 70:
        level = "보통"
    else:
        level = "부족"
    print(f"{subject}: {score}점 ({level})")

print("\n=== 실습 예제 3: 은행 대출 심사 시스템 ===")

age = 35
annual_income = 4500  # 만원
credit_score = 750
employment_period = 36  # 개월
loan_amount = 20000  # 만원

print("=== 대출 신청 정보 ===")
print(f"나이: {age}세")
print(f"연소득: {annual_income}만원")
print(f"신용점수: {credit_score}")
print(f"재직기간: {employment_period}개월")
print(f"대출희망금액: {loan_amount}만원")

print("\n=== 대출 심사 결과 ===")

# 기본 자격 요건 확인
if age < 20 or age > 65:
    print("연령 조건 불충족 (20세~65세)")
    loan_approved = False
elif annual_income < 2000:
    print("소득 조건 불충족 (연소득 2천만원 이상)")
    loan_approved = False
elif credit_score < 600:
    print("신용점수 조건 불충족 (600점 이상)")
    loan_approved = False
elif employment_period < 12:
    print("재직기간 조건 불충족 (12개월 이상)")
    loan_approved = False
else:
    # 대출 한도 계산
    if credit_score >= 800 and annual_income >= 5000:
        max_loan = annual_income * 6  # 연소득의 6배
        interest_rate = 2.5
    elif credit_score >= 700 and annual_income >= 3000:
        max_loan = annual_income * 5  # 연소득의 5배
        interest_rate = 3.2
    elif credit_score >= 650:
        max_loan = annual_income * 4  # 연소득의 4배
        interest_rate = 4.1
    else:
        max_loan = annual_income * 3  # 연소득의 3배
        interest_rate = 5.5
    
    if loan_amount <= max_loan:
        loan_approved = True
        print("대출 승인!")
        print(f"승인 금액: {loan_amount:,}만원")
        print(f"금리: {interest_rate}%")
        
        # 우대금리 적용
        if employment_period >= 60 and credit_score >= 750:
            interest_rate -= 0.5
            print("장기근속 우대금리 -0.5% 적용")
        
        print(f"최종 금리: {interest_rate}%")
    else:
        loan_approved = False
        print("대출 한도 초과")
        print(f"최대 가능 금액: {max_loan:,}만원")

print("\n=== 실습 예제 4: 놀이공원 입장료 계산 ===")

age = 8
is_student = True
is_group = True  # 10명 이상 단체
is_weekend = False
has_coupon = True

print("=== 놀이공원 입장료 계산 ===")
print(f"나이: {age}세")
print(f"학생: {'예' if is_student else '아니오'}")
print(f"단체: {'예' if is_group else '아니오'}")
print(f"주말: {'예' if is_weekend else '아니오'}")
print(f"쿠폰: {'예' if has_coupon else '아니오'}")

# 기본 요금 설정
if age < 3:
    base_price = 0
    category = "무료 (36개월 미만)"
elif age < 13:
    base_price = 25000
    category = "어린이"
elif age < 18:
    base_price = 35000
    category = "청소년"
elif age < 65:
    base_price = 45000
    category = "성인"
else:
    base_price = 25000
    category = "경로우대"

print(f"\n기본 요금: {base_price:,}원 ({category})")

# 할인 적용
discount_rate = 0
discount_reasons = []

if is_student and age >= 13:  # 중학생 이상 학생
    discount_rate += 0.1
    discount_reasons.append("학생할인 10%")

if is_group:
    discount_rate += 0.15
    discount_reasons.append("단체할인 15%")

if not is_weekend:  # 평일
    discount_rate += 0.2
    discount_reasons.append("평일할인 20%")

if has_coupon:
    discount_rate += 0.05
    discount_reasons.append("쿠폰할인 5%")

# 최대 할인율 제한
if discount_rate > 0.4:
    discount_rate = 0.4
    discount_reasons.append("(최대 40% 한도)")

# 최종 계산
discount_amount = base_price * discount_rate
final_price = base_price - discount_amount

print(f"\n적용 할인: {', '.join(discount_reasons) if discount_reasons else '없음'}")
print(f"할인율: {discount_rate*100:.0f}%")
print(f"할인금액: {discount_amount:,}원")
print(f"최종 입장료: {final_price:,}원")

# ===================================================================
# 7. 조건부 표현식 (Conditional Expression / Ternary Operator)
# ===================================================================

print("\n=== 조건부 표현식 (삼항 연산자) ===")

# 기본 형태: value_if_true if condition else value_if_false
age = 20
status = "성인" if age >= 18 else "미성년자"
print(f"나이 {age}세: {status}")

# 숫자 비교
a = 10
b = 20
max_value = a if a > b else b
print(f"{a}과 {b} 중 큰 수: {max_value}")

# 짝수/홀수
number = 7
parity = "짝수" if number % 2 == 0 else "홀수"
print(f"{number}은(는) {parity}")

# 절댓값 구하기
num = -15
absolute = num if num >= 0 else -num
print(f"{num}의 절댓값: {absolute}")

# 중첩된 조건부 표현식
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(f"점수 {score}: {grade}학점")

print("\n=== 5단계 완료! ===")
print("조건문을 모두 배웠습니다.")
print("다음 단계에서는 반복문을 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
5단계에서 기억해야 할 중요한 점들:

1. if문의 기본 구조: if 조건: (콜론 필수)
2. 들여쓰기 중요: 파이썬은 들여쓰기로 블록을 구분
3. elif는 else if의 줄임말
4. 조건은 True/False로 평가되는 모든 표현식 가능
5. 중첩 조건문: if 안에 if 사용 가능
6. 논리 연산자: and, or, not으로 복잡한 조건 표현
7. 조건부 표현식: 간단한 if-else를 한 줄로

실습할 때 꼭 해보세요:
- 다양한 조건으로 if문 만들어보기
- 복잡한 elif 체인 연습하기
- 중첩 조건문으로 복잡한 로직 구현
- 실생활 문제를 조건문으로 해결하기
- 논리 연산자 조합 연습하기
"""
