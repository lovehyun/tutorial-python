# 🎯 반드시 연습해야 할 핵심 개념들

#########################################################
# 1. 함수의 기본 구조
def function_name(parameter1, parameter2="default_value"):
    """함수 설명 (docstring)"""
    # 함수 내용
    result = parameter1 + parameter2
    return result  # 반환값

# 함수 호출
output = function_name(10, 20)


#########################################################
# 2. 매개변수의 다양한 형태
# 기본값이 있는 매개변수
def greet(name, title="님"):
    return f"안녕하세요, {name}{title}!"

# 가변 인수 (*args)
def sum_all(*numbers):
    return sum(numbers)

# 가변 키워드 인수 (**kwargs)  
def create_profile(**info):
    return info

# 사용 예
print(greet("김철수"))                    # 기본값 사용
print(sum_all(1, 2, 3, 4, 5))           # 여러 인수
print(create_profile(name="이영희", age=25))  # 키워드 인수


#########################################################
# 3. 함수의 반환값 활용
# 단일 값 반환
def calculate_area(radius):
    return 3.14159 * radius ** 2

# 여러 값 반환 (튜플로 패킹)
def get_name_age():
    return "김철수", 25

# 언패킹으로 받기
name, age = get_name_age()

# 조건부 반환
def check_password(password):
    if len(password) >= 8:
        return True, "강한 비밀번호"
    else:
        return False, "비밀번호가 너무 짧습니다"


#########################################################
# 4. 람다 함수 실전 활용
# 정렬에 활용
students = [("김철수", 85), ("이영희", 92), ("박민수", 78)]
sorted_by_score = sorted(students, key=lambda x: x[1])  # 점수순
sorted_by_name = sorted(students, key=lambda x: x[0])   # 이름순

# 필터링에 활용
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
squares = list(map(lambda x: x**2, numbers))


#########################################################
# 💡 함수 설계의 좋은 원칙들
#########################################################
# 1. 단일 책임 원칙
# 좋은 예: 하나의 기능만 담당
def calculate_tax(price, tax_rate):
    return price * tax_rate

def format_currency(amount):
    return f"{amount:,.0f}원"

# 나쁜 예: 여러 기능이 섞임
def calculate_and_display_tax(price, tax_rate):
    tax = price * tax_rate
    formatted = f"{tax:,.0f}원"
    print(f"세금: {formatted}")  # 계산과 출력이 섞임
    return tax


#########################################################
# 2. 의미 있는 함수명과 매개변수명
# 좋은 예
def convert_celsius_to_fahrenheit(celsius):
    return celsius * 9/5 + 32

# 나쁜 예
def convert(c):
    return c * 9/5 + 32


#########################################################
# 3. 기본값과 검증
def create_user_profile(name, age=None, email=None):
    # 입력값 검증
    if not name or not name.strip():
        raise ValueError("이름은 필수입니다")
    
    if age is not None and age < 0:
        raise ValueError("나이는 0 이상이어야 합니다")
    
    profile = {"name": name.strip()}
    
    if age is not None:
        profile["age"] = age
    if email:
        profile["email"] = email.strip().lower()
    
    return profile


#########################################################
# 🚨 초보자가 자주 하는 실수들
#########################################################
# 1. 가변 기본값 사용
# 위험한 패턴
def add_item(item, target_list=[]):  # 기본값이 가변 객체
    target_list.append(item)
    return target_list

# 첫 번째 호출
list1 = add_item("A")  # ["A"]
# 두 번째 호출  
list2 = add_item("B")  # ["A", "B"] - 예상과 다름!

# 안전한 패턴
def add_item_safe(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list


#########################################################
# 2. 전역변수 남용
# 나쁜 예
total = 0  # 전역변수

def add_to_total(value):
    global total
    total += value

# 좋은 예
def calculate_total(values):
    return sum(values)

# 또는 클래스 사용 (나중에 배울 내용)
class Calculator:
    def __init__(self):
        self.total = 0
    
    def add(self, value):
        self.total += value
        return self.total


#########################################################
# 3. return 문 누락
# 의도치 않은 None 반환
def calculate_discount(price, rate):
    discount = price * rate
    # return 문이 없음 - None이 반환됨

# 올바른 예
def calculate_discount(price, rate):
    discount = price * rate
    return discount


#########################################################
# 🔍 실무에서 자주 쓰이는 함수 패턴들
# 1. 유틸리티 함수
def is_valid_email(email):
    """이메일 유효성 검사"""
    return "@" in email and "." in email.split("@")[-1]

def format_phone_number(phone):
    """전화번호 포맷팅"""
    digits = "".join(filter(str.isdigit, phone))
    if len(digits) == 11:
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    return phone

def safe_divide(a, b):
    """안전한 나눗셈"""
    try:
        return a / b
    except ZeroDivisionError:
        return 0


#########################################################
# 2. 데이터 변환 함수
def parse_csv_line(line):
    """CSV 라인을 파싱"""
    return [item.strip() for item in line.split(",")]

def dict_to_query_string(data):
    """딕셔너리를 쿼리 스트링으로 변환"""
    pairs = [f"{key}={value}" for key, value in data.items()]
    return "&".join(pairs)

def flatten_list(nested_list):
    """중첩 리스트를 평탄화"""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


#########################################################
# 3. 검증 함수
def validate_password_strength(password):
    """비밀번호 강도 검증"""
    checks = {
        "길이": len(password) >= 8,
        "대문자": any(c.isupper() for c in password),
        "소문자": any(c.islower() for c in password),
        "숫자": any(c.isdigit() for c in password),
        "특수문자": any(c in "!@#$%^&*" for c in password)
    }
    
    passed = sum(checks.values())
    strength = ["매우 약함", "약함", "보통", "강함", "매우 강함"][min(passed, 4)]
    
    return {
        "strength": strength,
        "passed_checks": passed,
        "details": checks
    }


#########################################################
# 💪 함수를 활용한 프로젝트 아이디어
#########################################################
# 1. 텍스트 처리 도구모음
def text_toolkit():
    """텍스트 처리 도구들을 모아둔 함수"""
    
    def word_count(text):
        return len(text.split())
    
    def char_frequency(text):
        freq = {}
        for char in text.lower():
            if char.isalpha():
                freq[char] = freq.get(char, 0) + 1
        return dict(sorted(freq.items()))
    
    def extract_emails(text):
        import re
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    return {
        "word_count": word_count,
        "char_frequency": char_frequency,
        "extract_emails": extract_emails
    }


#########################################################
# 2. 게임 로직 함수들
def game_mechanics():
    """게임 메커니즘 함수들"""
    
    import random
    
    def roll_dice(num_dice=1, sides=6):
        return [random.randint(1, sides) for _ in range(num_dice)]
    
    def calculate_critical_hit(base_damage, crit_chance=0.1, crit_multiplier=2):
        if random.random() < crit_chance:
            return base_damage * crit_multiplier, True
        return base_damage, False
    
    def generate_random_name():
        prefixes = ["강력한", "신비로운", "어둠의", "빛나는", "전설의"]
        nouns = ["전사", "마법사", "궁수", "도적", "성기사"]
        return f"{random.choice(prefixes)} {random.choice(nouns)}"
    
    return {
        "roll_dice": roll_dice,
        "critical_hit": calculate_critical_hit,
        "random_name": generate_random_name
    }


#########################################################
# 3. 데이터 분석 헬퍼 함수들
def data_analysis_helpers():
    """데이터 분석을 위한 헬퍼 함수들"""
    
    def calculate_statistics(numbers):
        if not numbers:
            return None
        
        sorted_nums = sorted(numbers)
        n = len(numbers)
        
        return {
            "count": n,
            "sum": sum(numbers),
            "mean": sum(numbers) / n,
            "median": sorted_nums[n//2] if n % 2 == 1 else 
                     (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2,
            "min": min(numbers),
            "max": max(numbers),
            "range": max(numbers) - min(numbers)
        }
    
    def normalize_data(numbers, min_val=0, max_val=1):
        """데이터를 지정된 범위로 정규화"""
        if not numbers:
            return []
        
        data_min, data_max = min(numbers), max(numbers)
        if data_max == data_min:
            return [min_val] * len(numbers)
        
        scale = (max_val - min_val) / (data_max - data_min)
        return [min_val + (x - data_min) * scale for x in numbers]
    
    def group_by_range(numbers, range_size=10):
        """숫자들을 범위별로 그룹화"""
        groups = {}
        for num in numbers:
            range_start = (num // range_size) * range_size
            range_key = f"{range_start}-{range_start + range_size - 1}"
            
            if range_key not in groups:
                groups[range_key] = []
            groups[range_key].append(num)
        
        return groups
    
    return {
        "statistics": calculate_statistics,
        "normalize": normalize_data,
        "group_by_range": group_by_range
    }


#########################################################
# 🎯 함수 숙달을 위한 실습 과제
#########################################################
# 과제 1: 개인 맞춤 계산기
# 다음 기능들을 가진 계산기 함수들을 만들어보세요:
# 1. 기본 사칙연산 (add, subtract, multiply, divide)
# 2. 고급 연산 (power, sqrt, factorial)
# 3. 단위 변환 (celsius_to_fahrenheit, meters_to_feet)
# 4. 금융 계산 (compound_interest, loan_payment)

#########################################################
# 과제 2: 문자열 분석 도구
# 다음 기능들을 구현해보세요:
# 1. 가독성 점수 계산 (평균 단어 길이, 문장 길이)
# 2. 키워드 추출 (가장 빈번한 단어들)
# 3. 언어 감지 (한글/영어 비율)
# 4. 텍스트 요약 (첫 문장과 마지막 문장)

#########################################################
# 과제 3: 게임 시뮬레이터
# 간단한 RPG 게임 함수들:
# 1. 캐릭터 생성 (이름, 직업, 능력치)
# 2. 전투 시스템 (공격, 방어, 회복)
# 3. 레벨업 시스템 (경험치, 능력치 증가)
# 4. 아이템 시스템 (획득, 사용, 효과)


#########################################################
# 🏆 함수 마스터가 되기 위한 팁
#########################################################

# 작은 함수들을 많이 만들어보기: 큰 함수보다는 하나의 역할만 하는 작은 함수들이 좋습니다.
# 함수 이름을 신중하게 짓기: calculate_tax(), validate_email() 같이 목적이 명확한 이름을 사용하세요.
# docstring 작성 습관: 함수가 무엇을 하는지, 어떤 매개변수를 받는지, 무엇을 반환하는지 문서화하세요.
# 테스트 케이스 만들기: 다양한 입력값으로 함수를 테스트해보세요.
# 재사용성 고려하기: 한 번 만든 함수를 다른 프로젝트에서도 쓸 수 있도록 범용적으로 설계하세요.

