# ===================================================================
# 파이썬 9단계: 함수 실습 코드
# ===================================================================

# ===================================================================
# 1. 함수 정의와 호출 기본
# ===================================================================

print("=== 함수 기초 ===")

# 가장 간단한 함수
def say_hello():
    """인사말을 출력하는 함수"""
    print("안녕하세요!")

# 함수 호출
say_hello()
say_hello()  # 여러 번 호출 가능

# 매개변수가 있는 함수
def greet(name):
    """이름을 받아서 인사하는 함수"""
    print(f"안녕하세요, {name}님!")

greet("김파이썬")
greet("이자바")

# 여러 매개변수를 가진 함수
def introduce(name, age, city):
    """이름, 나이, 도시를 받아서 소개하는 함수"""
    print(f"제 이름은 {name}이고, {age}세이며, {city}에 살고 있습니다.")

introduce("박파이썬", 25, "서울")

# 기본값을 가진 매개변수
def greet_with_title(name, title="님"):
    """제목과 함께 인사하는 함수 (기본값 제공)"""
    print(f"안녕하세요, {name}{title}!")

greet_with_title("김철수")        # 기본값 사용
greet_with_title("이영희", "씨")   # 기본값 대신 다른 값 사용

print("\n=== 반환값이 있는 함수 ===")

# 값을 반환하는 함수
def add_numbers(a, b):
    """두 수를 더해서 결과를 반환하는 함수"""
    result = a + b
    return result

# 함수 호출하고 결과 받기
sum_result = add_numbers(10, 20)
print(f"10 + 20 = {sum_result}")

# 여러 값을 반환하는 함수
def calculate(a, b):
    """두 수의 사칙연산 결과를 모두 반환"""
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else 0
    
    return addition, subtraction, multiplication, division

# 여러 반환값 받기
add, sub, mul, div = calculate(20, 5)
print(f"20과 5의 연산 결과:")
print(f"덧셈: {add}, 뺄셈: {sub}, 곱셈: {mul}, 나눗셈: {div}")

# 조건에 따른 다른 반환값
def check_grade(score):
    """점수에 따라 학점을 반환하는 함수"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# 테스트
test_scores = [95, 87, 76, 65, 45]
for score in test_scores:
    grade = check_grade(score)
    print(f"점수 {score}: {grade}학점")

# ===================================================================
# 2. 매개변수와 인수의 다양한 형태
# ===================================================================

print("\n=== 매개변수 고급 사용법 ===")

# 위치 인수와 키워드 인수
def create_profile(name, age, city="서울", job="학생"):
    """프로필을 생성하는 함수"""
    profile = f"이름: {name}, 나이: {age}, 도시: {city}, 직업: {job}"
    return profile

# 다양한 호출 방법
print("위치 인수만:")
print(create_profile("김철수", 25))

print("\n키워드 인수 사용:")
print(create_profile("이영희", 30, job="개발자"))

print("\n키워드 인수로 순서 바꾸기:")
print(create_profile(city="부산", name="박민수", age=28, job="디자이너"))

# 가변 인수 (*args)
def sum_all(*numbers):
    """개수에 상관없이 모든 숫자를 더하는 함수"""
    total = 0
    for num in numbers:
        total += num
    return total

print(f"\n가변 인수 테스트:")
print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
print(f"sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
print(f"sum_all(10) = {sum_all(10)}")

# 가변 키워드 인수 (**kwargs)
def create_student(**info):
    """키워드 인수로 학생 정보를 생성하는 함수"""
    print("학생 정보:")
    for key, value in info.items():
        print(f"  {key}: {value}")

print(f"\n가변 키워드 인수 테스트:")
create_student(name="김파이썬", age=20, major="컴퓨터공학", gpa=3.8)

# 혼합 사용
def process_order(item_name, quantity, *extras, **details):
    """주문을 처리하는 함수 (모든 매개변수 형태 사용)"""
    print(f"주문 상품: {item_name}")
    print(f"수량: {quantity}")
    
    if extras:
        print(f"추가 옵션: {', '.join(extras)}")
    
    if details:
        print("상세 정보:")
        for key, value in details.items():
            print(f"  {key}: {value}")

print(f"\n복합 매개변수 테스트:")
process_order("피자", 2, "치즈추가", "매운맛", 
              delivery="빠른배송", payment="카드", note="문 앞에 놓아주세요")

# ===================================================================
# 3. 지역변수와 전역변수
# ===================================================================

print("\n=== 변수 스코프 (Scope) ===")

# 전역변수
global_var = "전역변수"

def scope_test():
    # 지역변수
    local_var = "지역변수"
    print(f"함수 내부에서: {global_var}")  # 전역변수 접근 가능
    print(f"함수 내부에서: {local_var}")   # 지역변수 접근

scope_test()
print(f"함수 외부에서: {global_var}")
# print(f"함수 외부에서: {local_var}")  # 에러! 지역변수는 접근 불가

# global 키워드 사용
counter = 0  # 전역변수

def increment():
    global counter  # 전역변수를 수정하겠다고 선언
    counter += 1
    print(f"카운터: {counter}")

print("전역변수 수정 테스트:")
increment()  # 1
increment()  # 2
increment()  # 3

# 지역변수와 전역변수 이름이 같은 경우
name = "전역 이름"

def name_test():
    name = "지역 이름"  # 새로운 지역변수 생성
    print(f"함수 내부: {name}")

name_test()
print(f"함수 외부: {name}")  # 전역변수는 변경되지 않음

# ===================================================================
# 4. 람다 함수 (Lambda Functions)
# ===================================================================

print("\n=== 람다 함수 ===")

# 기본 람다 함수
square = lambda x: x ** 2
print(f"lambda로 제곱: {square(5)}")

# 일반 함수와 비교
def square_normal(x):
    return x ** 2

print(f"일반 함수로 제곱: {square_normal(5)}")

# 여러 매개변수를 가진 람다
add = lambda x, y: x + y
multiply = lambda x, y, z: x * y * z

print(f"람다로 덧셈: {add(10, 20)}")
print(f"람다로 곱셈: {multiply(2, 3, 4)}")

# 람다와 내장 함수 조합
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map() 사용
squares = list(map(lambda x: x**2, numbers))
print(f"제곱수 리스트: {squares}")

# filter() 사용
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"짝수 리스트: {even_numbers}")

# sorted() 사용
students = [("김철수", 85), ("이영희", 92), ("박민수", 78)]
sorted_by_score = sorted(students, key=lambda student: student[1])
print(f"성적순 정렬: {sorted_by_score}")

sorted_by_name = sorted(students, key=lambda student: student[0])
print(f"이름순 정렬: {sorted_by_name}")

# ===================================================================
# 5. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 계산기 함수들 ===")

def calculator():
    """다양한 계산 기능을 제공하는 계산기"""
    
    def add(a, b):
        return a + b
    
    def subtract(a, b):
        return a - b
    
    def multiply(a, b):
        return a * b
    
    def divide(a, b):
        if b == 0:
            return "0으로 나눌 수 없습니다"
        return a / b
    
    def power(a, b):
        return a ** b
    
    def factorial(n):
        if n < 0:
            return "음수는 팩토리얼을 계산할 수 없습니다"
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    # 계산기 테스트
    operations = [
        ("덧셈", add, 10, 5),
        ("뺄셈", subtract, 10, 5),
        ("곱셈", multiply, 10, 5),
        ("나눗셈", divide, 10, 5),
        ("거듭제곱", power, 2, 3),
        ("팩토리얼", factorial, 5, None)
    ]
    
    for name, func, a, b in operations:
        if b is not None:
            result = func(a, b)
            print(f"{name}: {a}, {b} → {result}")
        else:
            result = func(a)
            print(f"{name}: {a} → {result}")

calculator()

print("\n=== 실습 예제 2: 텍스트 처리 함수들 ===")

def text_analyzer():
    """텍스트 분석 함수들"""
    
    def count_words(text):
        """단어 개수를 세는 함수"""
        return len(text.split())
    
    def count_characters(text, include_spaces=True):
        """문자 개수를 세는 함수"""
        if include_spaces:
            return len(text)
        else:
            return len(text.replace(" ", ""))
    
    def count_vowels(text):
        """모음 개수를 세는 함수"""
        vowels = "aeiouAEIOU"
        return sum(1 for char in text if char in vowels)
    
    def reverse_text(text):
        """텍스트를 뒤집는 함수"""
        return text[::-1]
    
    def capitalize_words(text):
        """각 단어의 첫 글자를 대문자로 만드는 함수"""
        return text.title()
    
    def remove_duplicates(text):
        """중복된 문자를 제거하는 함수"""
        seen = set()
        result = ""
        for char in text:
            if char not in seen:
                result += char
                seen.add(char)
        return result
    
    # 테스트 텍스트
    test_text = "Hello World Python Programming"
    
    print(f"원본 텍스트: '{test_text}'")
    print(f"단어 개수: {count_words(test_text)}")
    print(f"문자 개수 (공백 포함): {count_characters(test_text, True)}")
    print(f"문자 개수 (공백 제외): {count_characters(test_text, False)}")
    print(f"모음 개수: {count_vowels(test_text)}")
    print(f"텍스트 뒤집기: '{reverse_text(test_text)}'")
    print(f"단어 첫글자 대문자: '{capitalize_words(test_text.lower())}'")
    print(f"중복 문자 제거: '{remove_duplicates(test_text)}'")

text_analyzer()

print("\n=== 실습 예제 3: 학생 성적 관리 시스템 ===")

def grade_management_system():
    """학생 성적 관리 시스템"""
    
    # 학생 데이터 (전역적으로 관리)
    students = {}
    
    def add_student(student_id, name):
        """학생을 추가하는 함수"""
        students[student_id] = {
            "name": name,
            "grades": {}
        }
        return f"학생 {name}(ID: {student_id})이 추가되었습니다."
    
    def add_grade(student_id, subject, score):
        """성적을 추가하는 함수"""
        if student_id not in students:
            return "존재하지 않는 학생입니다."
        
        students[student_id]["grades"][subject] = score
        return f"성적이 추가되었습니다: {subject} - {score}점"
    
    def get_average(student_id):
        """평균 성적을 계산하는 함수"""
        if student_id not in students:
            return "존재하지 않는 학생입니다."
        
        grades = students[student_id]["grades"]
        if not grades:
            return "등록된 성적이 없습니다."
        
        average = sum(grades.values()) / len(grades)
        return round(average, 1)
    
    def get_grade_report(student_id):
        """성적표를 생성하는 함수"""
        if student_id not in students:
            return "존재하지 않는 학생입니다."
        
        student = students[student_id]
        name = student["name"]
        grades = student["grades"]
        
        if not grades:
            return f"{name} 학생의 등록된 성적이 없습니다."
        
        report = f"\n=== {name} 학생 성적표 ===\n"
        for subject, score in grades.items():
            report += f"{subject}: {score}점\n"
        
        average = get_average(student_id)
        report += f"평균: {average}점\n"
        
        # 학점 계산
        if average >= 90:
            grade = "A"
        elif average >= 80:
            grade = "B"
        elif average >= 70:
            grade = "C"
        elif average >= 60:
            grade = "D"
        else:
            grade = "F"
        
        report += f"학점: {grade}\n"
        return report
    
    def get_class_statistics():
        """전체 반 통계를 계산하는 함수"""
        if not students:
            return "등록된 학생이 없습니다."
        
        all_averages = []
        for student_id in students:
            avg = get_average(student_id)
            if isinstance(avg, (int, float)):
                all_averages.append(avg)
        
        if not all_averages:
            return "성적이 등록된 학생이 없습니다."
        
        class_average = sum(all_averages) / len(all_averages)
        highest = max(all_averages)
        lowest = min(all_averages)
        
        return f"""
=== 반 전체 통계 ===
학생 수: {len(students)}명
반 평균: {class_average:.1f}점
최고점: {highest}점
최저점: {lowest}점
        """.strip()
    
    # 시스템 테스트
    print("=== 학생 성적 관리 시스템 테스트 ===")
    
    # 학생 추가
    print(add_student("2024001", "김철수"))
    print(add_student("2024002", "이영희"))
    print(add_student("2024003", "박민수"))
    
    # 성적 추가
    print(add_grade("2024001", "수학", 85))
    print(add_grade("2024001", "영어", 92))
    print(add_grade("2024001", "과학", 78))
    
    print(add_grade("2024002", "수학", 95))
    print(add_grade("2024002", "영어", 88))
    print(add_grade("2024002", "과학", 92))
    
    print(add_grade("2024003", "수학", 76))
    print(add_grade("2024003", "영어", 82))
    print(add_grade("2024003", "과학", 79))
    
    # 성적표 출력
    print(get_grade_report("2024001"))
    print(get_grade_report("2024002"))
    print(get_grade_report("2024003"))
    
    # 반 통계
    print(get_class_statistics())

grade_management_system()

print("\n=== 실습 예제 4: 게임 함수들 ===")

def game_functions():
    """게임 관련 함수들"""
    
    import random
    
    def dice_roll(sides=6):
        """주사위를 굴리는 함수"""
        return random.randint(1, sides)
    
    def coin_flip():
        """동전 던지기 함수"""
        return random.choice(["앞면", "뒷면"])
    
    def rock_paper_scissors_judge(player1, player2):
        """가위바위보 승부 판정 함수"""
        choices = {"가위": 1, "바위": 2, "보": 3}
        
        if player1 not in choices or player2 not in choices:
            return "잘못된 선택입니다"
        
        if player1 == player2:
            return "무승부"
        elif (choices[player1] == 1 and choices[player2] == 3) or \
             (choices[player1] == 2 and choices[player2] == 1) or \
             (choices[player1] == 3 and choices[player2] == 2):
            return "플레이어1 승리"
        else:
            return "플레이어2 승리"
    
    def generate_lottery_numbers(count=6, max_number=45):
        """로또 번호 생성 함수"""
        numbers = random.sample(range(1, max_number + 1), count)
        return sorted(numbers)
    
    def calculate_damage(attack, defense, critical_chance=0.1):
        """RPG 게임 데미지 계산 함수"""
        base_damage = max(1, attack - defense)
        
        # 크리티컬 히트 확인
        if random.random() < critical_chance:
            base_damage *= 2
            return base_damage, True  # 데미지, 크리티컬 여부
        
        return base_damage, False
    
    # 게임 함수들 테스트
    print("=== 게임 함수들 테스트 ===")
    
    # 주사위 굴리기
    print(f"6면 주사위: {dice_roll()}")
    print(f"20면 주사위: {dice_roll(20)}")
    
    # 동전 던지기
    print(f"동전 던지기: {coin_flip()}")
    
    # 가위바위보
    choices = ["가위", "바위", "보"]
    p1_choice = random.choice(choices)
    p2_choice = random.choice(choices)
    result = rock_paper_scissors_judge(p1_choice, p2_choice)
    print(f"가위바위보: {p1_choice} vs {p2_choice} → {result}")
    
    # 로또 번호
    lottery = generate_lottery_numbers()
    print(f"로또 번호: {lottery}")
    
    # 데미지 계산
    damage, is_critical = calculate_damage(50, 20, 0.3)
    crit_text = " (크리티컬!)" if is_critical else ""
    print(f"데미지: {damage}{crit_text}")

game_functions()

# ===================================================================
# 6. 함수형 프로그래밍 기초
# ===================================================================

print("\n=== 함수형 프로그래밍 기초 ===")

# 고차 함수 (함수를 인수로 받는 함수)
def apply_operation(numbers, operation):
    """리스트의 모든 숫자에 연산을 적용하는 함수"""
    return [operation(num) for num in numbers]

# 연산 함수들
def square(x):
    return x ** 2

def double(x):
    return x * 2

def is_even(x):
    return x % 2 == 0

# 테스트
numbers = [1, 2, 3, 4, 5]
print(f"원본: {numbers}")
print(f"제곱: {apply_operation(numbers, square)}")
print(f"2배: {apply_operation(numbers, double)}")

# filter와 map 활용
print(f"짝수만: {list(filter(is_even, numbers))}")
print(f"모든 수 제곱: {list(map(square, numbers))}")

# 함수를 반환하는 함수
def create_multiplier(factor):
    """지정된 배수를 만드는 함수를 생성하는 함수"""
    def multiplier(x):
        return x * factor
    return multiplier

# 사용 예
triple = create_multiplier(3)
quintuple = create_multiplier(5)

print(f"3배 함수: {triple(10)}")  # 30
print(f"5배 함수: {quintuple(10)}")  # 50

# 데코레이터 기초 개념
def timer_decorator(func):
    """함수 실행 시간을 측정하는 데코레이터"""
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 실행 시간: {end_time - start_time:.4f}초")
        return result
    
    return wrapper

# 데코레이터 사용 (고급 개념이므로 참고용)
@timer_decorator
def slow_function():
    """시간이 걸리는 함수 (시뮬레이션)"""
    import time
    time.sleep(0.1)  # 0.1초 대기
    return "작업 완료"

print("데코레이터 테스트:")
result = slow_function()
print(f"결과: {result}")

# ===================================================================
# 7. 함수 문서화 (Docstring)
# ===================================================================

print("\n=== 함수 문서화 ===")

def calculate_bmi(weight, height):
    """
    BMI(체질량지수)를 계산하는 함수
    
    Args:
        weight (float): 체중 (kg)
        height (float): 키 (m)
    
    Returns:
        tuple: (BMI 값, 분류) 튜플
        
    Example:
        >>> bmi, category = calculate_bmi(70, 1.75)
        >>> print(f"BMI: {bmi:.1f}, 분류: {category}")
    """
    if height <= 0 or weight <= 0:
        return None, "잘못된 입력값"
    
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        category = "저체중"
    elif bmi < 25:
        category = "정상"
    elif bmi < 30:
        category = "과체중"
    else:
        category = "비만"
    
    return round(bmi, 1), category

# 함수 문서 확인
print(f"함수 이름: {calculate_bmi.__name__}")
print(f"함수 문서:\n{calculate_bmi.__doc__}")

# 함수 사용
bmi, category = calculate_bmi(70, 1.75)
print(f"BMI 계산 결과: {bmi}, 분류: {category}")

print("\n=== 9단계 완료! ===")
print("함수를 모두 배웠습니다.")
print("다음 단계에서는 예외 처리를 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
9단계에서 기억해야 할 중요한 점들:

1. 함수 정의: def 함수명(매개변수):
2. 반환값: return 문 사용 (없으면 None 반환)
3. 매개변수 종류:
   - 위치 매개변수: func(a, b)
   - 기본값 매개변수: func(a, b=10)
   - 가변 매개변수: func(*args, **kwargs)

4. 변수 스코프:
   - 지역변수: 함수 내부에서만 사용
   - 전역변수: global 키워드로 수정 가능

5. 람다 함수: lambda x: x**2 (간단한 함수)

6. 함수형 프로그래밍:
   - map(), filter(), sorted() 등과 함께 사용
   - 함수를 변수에 저장하고 인수로 전달 가능

7. 문서화: docstring으로 함수 설명 작성

실습할 때 꼭 해보세요:
- 자주 사용하는 코드를 함수로 만들어보기
- 매개변수와 반환값을 다양하게 활용하기
- 람다 함수로 간단한 연산 만들기
- 함수를 조합해서 복잡한 프로그램 구성하기
- docstring으로 함수 문서화하기
"""
