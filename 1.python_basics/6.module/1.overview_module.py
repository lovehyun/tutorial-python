# ===================================================================
# 파이썬 12단계: 모듈과 패키지 실습 코드
# ===================================================================

# ===================================================================
# 1. 모듈 import하기 기본
# ===================================================================

print("=== 모듈 import 기본 ===")

# 1. 전체 모듈 import
import math
import random
import datetime

print("전체 모듈 import:")
print(f"원주율: {math.pi}")
print(f"제곱근: {math.sqrt(16)}")
print(f"랜덤 숫자: {random.randint(1, 100)}")
print(f"현재 시간: {datetime.datetime.now()}")

# 2. 특정 함수만 import
from math import sin, cos, tan, pi
from random import choice, shuffle
from datetime import date, timedelta

print(f"\n특정 함수만 import:")
print(f"sin(π/2): {sin(pi/2)}")
print(f"cos(0): {cos(0)}")

colors = ["빨강", "파랑", "노랑", "초록"]
print(f"랜덤 색상: {choice(colors)}")

today = date.today()
tomorrow = today + timedelta(days=1)
print(f"오늘: {today}, 내일: {tomorrow}")

# 3. 별칭 사용 (alias)
import numpy as np  # numpy가 설치되어 있다면
import pandas as pd  # pandas가 설치되어 있다면
import matplotlib.pyplot as plt  # matplotlib이 설치되어 있다면

# 실제로는 이렇게 사용하지만, 예제에서는 주석 처리
# print(f"NumPy 배열: {np.array([1, 2, 3, 4, 5])}")

# 4. 모든 것 import (권장하지 않음)
# from math import *  # 이름 충돌 위험이 있어서 권장하지 않음

print("\n=== 모듈 import 방식 비교 ===")

# 방식 1: import module
import os
current_dir = os.getcwd()
print(f"현재 디렉토리 (os.getcwd()): {current_dir}")

# 방식 2: from module import function
from os import getcwd
current_dir2 = getcwd()
print(f"현재 디렉토리 (getcwd()): {current_dir2}")

# 방식 3: import module as alias
import os as operating_system
current_dir3 = operating_system.getcwd()
print(f"현재 디렉토리 (operating_system.getcwd()): {current_dir3}")

# ===================================================================
# 2. 표준 라이브러리 활용
# ===================================================================

print("\n=== 표준 라이브러리 활용 ===")

# math 모듈 - 수학 함수들
print("=== math 모듈 ===")
import math

numbers = [4, 9, 16, 25]
print(f"숫자들: {numbers}")
print(f"제곱근들: {[math.sqrt(n) for n in numbers]}")
print(f"로그값들: {[math.log(n) for n in numbers]}")

# 삼각함수
angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2]
print(f"각도들 (라디안): {[round(a, 2) for a in angles]}")
print(f"사인값들: {[round(math.sin(a), 2) for a in angles]}")

# random 모듈 - 난수 생성
print("\n=== random 모듈 ===")
import random

# 기본 랜덤 함수들
print(f"0~1 사이 실수: {random.random()}")
print(f"1~10 사이 정수: {random.randint(1, 10)}")
print(f"1~10 사이 실수: {random.uniform(1, 10)}")

# 리스트에서 선택
fruits = ["사과", "바나나", "오렌지", "포도", "딸기"]
print(f"과일들: {fruits}")
print(f"랜덤 과일: {random.choice(fruits)}")
print(f"랜덤 과일 3개: {random.sample(fruits, 3)}")

# 리스트 섞기
numbers = list(range(1, 11))
print(f"원본 숫자: {numbers}")
random.shuffle(numbers)
print(f"섞인 숫자: {numbers}")

# datetime 모듈 - 날짜와 시간
print("\n=== datetime 모듈 ===")
from datetime import datetime, date, time, timedelta

# 현재 날짜와 시간
now = datetime.now()
today = date.today()
current_time = datetime.now().time()

print(f"현재 날짜시간: {now}")
print(f"오늘 날짜: {today}")
print(f"현재 시간: {current_time}")

# 날짜 계산
yesterday = today - timedelta(days=1)
next_week = today + timedelta(weeks=1)
print(f"어제: {yesterday}")
print(f"다음 주: {next_week}")

# 날짜 포맷팅
print(f"포맷된 날짜: {now.strftime('%Y년 %m월 %d일 %H시 %M분')}")

# os 모듈 - 운영체제 인터페이스
print("\n=== os 모듈 ===")
import os

print(f"현재 작업 디렉토리: {os.getcwd()}")
print(f"홈 디렉토리: {os.path.expanduser('~')}")
print(f"경로 구분자: '{os.sep}'")

# 환경 변수
print(f"PATH 환경변수 일부: {os.environ.get('PATH', '없음')[:50]}...")

# 경로 조작
file_path = os.path.join("folder", "subfolder", "file.txt")
print(f"조합된 경로: {file_path}")
print(f"디렉토리명: {os.path.dirname(file_path)}")
print(f"파일명: {os.path.basename(file_path)}")

# sys 모듈 - 시스템 정보
print("\n=== sys 모듈 ===")
import sys

print(f"파이썬 버전: {sys.version}")
print(f"플랫폼: {sys.platform}")
print(f"모듈 검색 경로 수: {len(sys.path)}")

# json 모듈 - JSON 처리
print("\n=== json 모듈 ===")
import json

# Python 객체를 JSON으로
student = {
    "name": "김파이썬",
    "age": 25,
    "courses": ["Python", "JavaScript", "SQL"],
    "graduated": False
}

json_string = json.dumps(student, ensure_ascii=False, indent=2)
print(f"JSON 문자열:\n{json_string}")

# JSON을 Python 객체로
parsed_student = json.loads(json_string)
print(f"파싱된 객체: {parsed_student['name']}")

# ===================================================================
# 3. 사용자 정의 모듈 만들기
# ===================================================================

print("\n=== 사용자 정의 모듈 만들기 ===")

# 실제 프로젝트에서는 별도 파일로 만들지만, 
# 여기서는 예제를 위해 문자열로 모듈 내용을 보여드립니다.

# calculator.py 모듈 예제
calculator_module_content = '''
"""
calculator.py - 간단한 계산기 모듈

이 모듈은 기본적인 수학 연산 함수들을 제공합니다.
"""

def add(a, b):
    """두 수를 더합니다."""
    return a + b

def subtract(a, b):
    """첫 번째 수에서 두 번째 수를 뺍니다."""
    return a - b

def multiply(a, b):
    """두 수를 곱합니다."""
    return a * b

def divide(a, b):
    """첫 번째 수를 두 번째 수로 나눕니다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b

def power(base, exponent):
    """거듭제곱을 계산합니다."""
    return base ** exponent

# 모듈 변수
PI = 3.14159265359
E = 2.71828182846

# 모듈이 직접 실행될 때만 실행되는 코드
if __name__ == "__main__":
    print("계산기 모듈 테스트")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"5 * 6 = {multiply(5, 6)}")
    print(f"15 / 3 = {divide(15, 3)}")
'''

# calculator.py 파일 생성
with open("calculator.py", "w", encoding="utf-8") as f:
    f.write(calculator_module_content)

print("✅ calculator.py 모듈이 생성되었습니다.")

# utils.py 모듈 예제
utils_module_content = '''
"""
utils.py - 유틸리티 함수 모듈

자주 사용되는 유틸리티 함수들을 모아둔 모듈입니다.
"""

def is_even(number):
    """숫자가 짝수인지 확인합니다."""
    return number % 2 == 0

def is_prime(number):
    """숫자가 소수인지 확인합니다."""
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def factorial(n):
    """팩토리얼을 계산합니다."""
    if n < 0:
        raise ValueError("음수의 팩토리얼은 정의되지 않습니다")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(n):
    """n번째 피보나치 수를 반환합니다."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def format_number(number, decimal_places=2):
    """숫자를 보기 좋게 포맷합니다."""
    return f"{number:,.{decimal_places}f}"

# 상수들
MAX_INT = 2**31 - 1
MIN_INT = -2**31

class Timer:
    """간단한 타이머 클래스"""
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """타이머를 시작합니다."""
        import time
        self.start_time = time.time()
        print("타이머 시작!")
    
    def stop(self):
        """타이머를 중지하고 경과 시간을 반환합니다."""
        import time
        if self.start_time is None:
            print("타이머가 시작되지 않았습니다.")
            return 0
        
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"경과 시간: {elapsed:.2f}초")
        return elapsed
'''

# utils.py 파일 생성
with open("utils.py", "w", encoding="utf-8") as f:
    f.write(utils_module_content)

print("✅ utils.py 모듈이 생성되었습니다.")

# 생성된 모듈 사용해보기
print("\n=== 생성된 모듈 사용하기 ===")

# calculator 모듈 사용
import calculator

print("계산기 모듈 테스트:")
print(f"5 + 3 = {calculator.add(5, 3)}")
print(f"10 - 4 = {calculator.subtract(10, 4)}")
print(f"6 * 7 = {calculator.multiply(6, 7)}")
print(f"15 / 3 = {calculator.divide(15, 3)}")
print(f"2^8 = {calculator.power(2, 8)}")
print(f"파이 값: {calculator.PI}")

# utils 모듈 사용
import utils

print(f"\n유틸리티 모듈 테스트:")
numbers = [10, 15, 17, 20, 23]
for num in numbers:
    even = "짝수" if utils.is_even(num) else "홀수"
    prime = "소수" if utils.is_prime(num) else "합성수"
    print(f"{num}: {even}, {prime}")

print(f"5! = {utils.factorial(5)}")
print(f"10번째 피보나치 수: {utils.fibonacci(10)}")
print(f"큰 숫자 포맷: {utils.format_number(1234567.89)}")

# Timer 클래스 사용
timer = utils.Timer()
timer.start()
import time
time.sleep(0.1)  # 0.1초 대기
timer.stop()

# ===================================================================
# 4. 패키지 만들기
# ===================================================================

print("\n=== 패키지 만들기 ===")

# 패키지 구조 생성
import os

# 메인 패키지 디렉토리
package_name = "mypackage"
if not os.path.exists(package_name):
    os.makedirs(package_name)

# 서브 패키지들
subpackages = ["math_tools", "string_tools", "file_tools"]
for subpkg in subpackages:
    subpkg_path = os.path.join(package_name, subpkg)
    if not os.path.exists(subpkg_path):
        os.makedirs(subpkg_path)

print(f"✅ 패키지 구조가 생성되었습니다: {package_name}/")

# __init__.py 파일들 생성
# 메인 패키지의 __init__.py
main_init_content = '''
"""
mypackage - 사용자 정의 패키지

이 패키지는 다양한 유틸리티 도구들을 제공합니다.
"""

__version__ = "1.0.0"
__author__ = "파이썬 학습자"

# 패키지 레벨에서 주요 함수들을 바로 사용할 수 있게 함
from .math_tools.basic import add, multiply
from .string_tools.text import reverse_string, count_words

print("mypackage가 import되었습니다!")
'''

with open(os.path.join(package_name, "__init__.py"), "w", encoding="utf-8") as f:
    f.write(main_init_content)

# math_tools 서브패키지
math_init_content = '''
"""
math_tools - 수학 관련 도구들
"""

from .basic import add, subtract, multiply, divide
from .advanced import factorial, fibonacci, is_prime
'''

with open(os.path.join(package_name, "math_tools", "__init__.py"), "w", encoding="utf-8") as f:
    f.write(math_init_content)

# math_tools/basic.py
math_basic_content = '''
"""
기본 수학 연산 함수들
"""

def add(a, b):
    """두 수를 더합니다."""
    return a + b

def subtract(a, b):
    """두 수를 뺍니다."""
    return a - b

def multiply(a, b):
    """두 수를 곱합니다."""
    return a * b

def divide(a, b):
    """두 수를 나눕니다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b
'''

with open(os.path.join(package_name, "math_tools", "basic.py"), "w", encoding="utf-8") as f:
    f.write(math_basic_content)

# math_tools/advanced.py
math_advanced_content = '''
"""
고급 수학 함수들
"""

def factorial(n):
    """팩토리얼을 계산합니다."""
    if n < 0:
        raise ValueError("음수의 팩토리얼은 정의되지 않습니다")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(n):
    """n번째 피보나치 수를 계산합니다."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def is_prime(number):
    """소수인지 확인합니다."""
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def gcd(a, b):
    """최대공약수를 계산합니다."""
    while b:
        a, b = b, a % b
    return a
'''

with open(os.path.join(package_name, "math_tools", "advanced.py"), "w", encoding="utf-8") as f:
    f.write(math_advanced_content)

# string_tools 서브패키지
string_init_content = '''
"""
string_tools - 문자열 처리 도구들
"""

from .text import reverse_string, count_words, capitalize_words
from .validation import is_email, is_phone_number
'''

with open(os.path.join(package_name, "string_tools", "__init__.py"), "w", encoding="utf-8") as f:
    f.write(string_init_content)

# string_tools/text.py
string_text_content = '''
"""
텍스트 처리 함수들
"""

def reverse_string(text):
    """문자열을 뒤집습니다."""
    return text[::-1]

def count_words(text):
    """문자열의 단어 수를 셉니다."""
    return len(text.split())

def capitalize_words(text):
    """각 단어의 첫 글자를 대문자로 만듭니다."""
    return text.title()

def remove_spaces(text):
    """모든 공백을 제거합니다."""
    return text.replace(" ", "")

def word_frequency(text):
    """단어 빈도를 계산합니다."""
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency
'''

with open(os.path.join(package_name, "string_tools", "text.py"), "w", encoding="utf-8") as f:
    f.write(string_text_content)

# string_tools/validation.py
string_validation_content = '''
"""
문자열 검증 함수들
"""

import re

def is_email(email):
    """이메일 형식인지 확인합니다."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_phone_number(phone):
    """전화번호 형식인지 확인합니다."""
    # 한국 전화번호 패턴 (010-1234-5678)
    pattern = r'^010-\d{4}-\d{4}$'
    return bool(re.match(pattern, phone))

def is_strong_password(password):
    """강한 비밀번호인지 확인합니다."""
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=" for c in password)
    
    return has_upper and has_lower and has_digit and has_special
'''

with open(os.path.join(package_name, "string_tools", "validation.py"), "w", encoding="utf-8") as f:
    f.write(string_validation_content)

# file_tools 서브패키지
file_init_content = '''
"""
file_tools - 파일 처리 도구들
"""

from .file_operations import read_file, write_file, copy_file
from .file_info import get_file_size, get_file_date
'''

with open(os.path.join(package_name, "file_tools", "__init__.py"), "w", encoding="utf-8") as f:
    f.write(file_init_content)

# file_tools/file_operations.py
file_operations_content = '''
"""
파일 조작 함수들
"""

import os
import shutil

def read_file(filepath, encoding='utf-8'):
    """파일을 읽습니다."""
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return None

def write_file(filepath, content, encoding='utf-8'):
    """파일에 내용을 씁니다."""
    try:
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"파일 쓰기 오류: {e}")
        return False

def copy_file(source, destination):
    """파일을 복사합니다."""
    try:
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"파일 복사 오류: {e}")
        return False

def delete_file(filepath):
    """파일을 삭제합니다."""
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        print(f"파일 삭제 오류: {e}")
        return False
'''

with open(os.path.join(package_name, "file_tools", "file_operations.py"), "w", encoding="utf-8") as f:
    f.write(file_operations_content)

# file_tools/file_info.py
file_info_content = '''
"""
파일 정보 조회 함수들
"""

import os
from datetime import datetime

def get_file_size(filepath):
    """파일 크기를 반환합니다."""
    try:
        return os.path.getsize(filepath)
    except Exception as e:
        print(f"파일 크기 조회 오류: {e}")
        return 0

def get_file_date(filepath):
    """파일 수정 날짜를 반환합니다."""
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"파일 날짜 조회 오류: {e}")
        return None

def file_exists(filepath):
    """파일이 존재하는지 확인합니다."""
    return os.path.exists(filepath)

def get_file_extension(filepath):
    """파일 확장자를 반환합니다."""
    return os.path.splitext(filepath)[1]

def list_files(directory, extension=None):
    """디렉토리의 파일 목록을 반환합니다."""
    try:
        files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                if extension is None or filename.endswith(extension):
                    files.append(filename)
        return files
    except Exception as e:
        print(f"파일 목록 조회 오류: {e}")
        return []
'''

with open(os.path.join(package_name, "file_tools", "file_info.py"), "w", encoding="utf-8") as f:
    f.write(file_info_content)

print("✅ 모든 패키지 파일들이 생성되었습니다.")

# 패키지 구조 출력
def print_directory_structure(path, prefix=""):
    """디렉토리 구조를 출력합니다."""
    items = sorted(os.listdir(path))
    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last = i == len(items) - 1
        
        if os.path.isdir(item_path):
            print(f"{prefix}{'└── ' if is_last else '├── '}{item}/")
            extension = "    " if is_last else "│   "
            print_directory_structure(item_path, prefix + extension)
        else:
            print(f"{prefix}{'└── ' if is_last else '├── '}{item}")

print(f"\n생성된 패키지 구조:")
print(f"{package_name}/")
print_directory_structure(package_name, "")

# ===================================================================
# 5. 패키지 사용하기
# ===================================================================

print("\n=== 패키지 사용하기 ===")

# 패키지 import (sys.path에 현재 디렉토리가 포함되어 있어야 함)
import sys
if "." not in sys.path:
    sys.path.insert(0, ".")

try:
    # 전체 패키지 import
    import mypackage
    
    print("패키지 import 성공!")
    print(f"패키지 버전: {mypackage.__version__}")
    print(f"패키지 작성자: {mypackage.__author__}")
    
    # 패키지에서 바로 사용할 수 있는 함수들
    result1 = mypackage.add(10, 5)
    result2 = mypackage.multiply(3, 7)
    print(f"패키지 레벨 함수: add(10, 5) = {result1}")
    print(f"패키지 레벨 함수: multiply(3, 7) = {result2}")
    
    # 서브패키지 import
    from mypackage.math_tools import advanced
    from mypackage.string_tools import text, validation
    from mypackage.file_tools import file_info
    
    # math_tools 사용
    print(f"\n수학 도구 사용:")
    print(f"5! = {advanced.factorial(5)}")
    print(f"10번째 피보나치 수: {advanced.fibonacci(10)}")
    print(f"17은 소수인가? {advanced.is_prime(17)}")
    
    # string_tools 사용
    print(f"\n문자열 도구 사용:")
    sample_text = "Hello Python World"
    print(f"원본: '{sample_text}'")
    print(f"뒤집기: '{text.reverse_string(sample_text)}'")
    print(f"단어 수: {text.count_words(sample_text)}")
    
    # 검증 도구 사용
    emails = ["test@example.com", "invalid.email", "user@domain.co.kr"]
    phones = ["010-1234-5678", "02-123-4567", "010-12-3456"]
    
    print(f"\n이메일 검증:")
    for email in emails:
        valid = validation.is_email(email)
        print(f"  {email}: {'유효' if valid else '무효'}")
    
    print(f"\n전화번호 검증:")
    for phone in phones:
        valid = validation.is_phone_number(phone)
        print(f"  {phone}: {'유효' if valid else '무효'}")
    
    # file_tools 사용
    print(f"\n파일 도구 사용:")
    current_files = file_info.list_files(".", ".py")
    print(f"현재 디렉토리의 Python 파일들:")
    for file in current_files[:5]:  # 처음 5개만 표시
        size = file_info.get_file_size(file)
        print(f"  {file}: {size} bytes")

except ImportError as e:
    print(f"패키지 import 오류: {e}")
    print("패키지가 제대로 생성되지 않았을 수 있습니다.")

# ===================================================================
# 6. pip 패키지 관리
# ===================================================================

print("\n=== pip 패키지 관리 ===")

# pip 명령어들 (실제로는 터미널에서 실행)
pip_commands = """
주요 pip 명령어들:

1. 패키지 설치:
   pip install 패키지명
   pip install requests numpy pandas

2. 특정 버전 설치:
   pip install 패키지명==버전
   pip install django==3.2.0

3. 패키지 업그레이드:
   pip install --upgrade 패키지명
   pip install -U numpy

4. 패키지 제거:
   pip uninstall 패키지명

5. 설치된 패키지 목록:
   pip list
   pip freeze

6. 패키지 정보 확인:
   pip show 패키지명

7. requirements.txt 사용:
   pip install -r requirements.txt
   pip freeze > requirements.txt

8. 가상환경에서 패키지 관리:
   python -m venv myenv
   source myenv/bin/activate  # Linux/Mac
   myenv\\Scripts\\activate   # Windows
   pip install 패키지명
   deactivate
"""

print(pip_commands)

# requirements.txt 파일 예제 생성
requirements_content = """# 프로젝트 의존성 패키지들
requests==2.28.1
numpy==1.21.0
pandas==1.3.3
matplotlib==3.5.2
flask==2.2.2
django==4.1.0
beautifulsoup4==4.11.1
selenium==4.5.0
pytest==7.1.3
black==22.8.0

# 개발용 패키지들 (선택사항)
# jupyter==1.0.0
# ipython==8.5.0
"""

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements_content)

print("✅ requirements.txt 파일이 생성되었습니다.")

# 현재 설치된 주요 패키지들 확인 (시뮬레이션)
def simulate_pip_list():
    """pip list 명령어 시뮬레이션"""
    print("\n현재 설치된 패키지들 (시뮬레이션):")
    print("Package         Version")
    print("-" * 30)
    
    # 실제로는 pip list의 결과이지만, 예제용으로 시뮬레이션
    simulated_packages = [
        ("pip", "22.3.1"),
        ("setuptools", "65.5.0"),
        ("wheel", "0.38.4"),
        # 추가 패키지들은 실제 환경에 따라 다름
    ]
    
    for package, version in simulated_packages:
        print(f"{package:<15} {version}")

simulate_pip_list()

# ===================================================================
# 7. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 개인 유틸리티 라이브러리 ===")

# personal_utils 패키지 생성
personal_utils_structure = {
    "personal_utils": {
        "__init__.py": '''
"""
personal_utils - 개인용 유틸리티 라이브러리

자주 사용하는 개인적인 도구들을 모아둔 패키지입니다.
"""

__version__ = "0.1.0"

# 자주 사용하는 함수들을 패키지 레벨에서 바로 접근 가능하게 함
from .time_utils import get_current_time, format_duration
from .text_utils import clean_text, extract_numbers
from .math_utils import round_smart, percentage

# 패키지 설정
DEFAULT_ENCODING = "utf-8"
DEBUG = False
''',
        "time_utils.py": '''
"""
시간 관련 유틸리티 함수들
"""

from datetime import datetime, timedelta
import time

def get_current_time(format_string="%Y-%m-%d %H:%M:%S"):
    """현재 시간을 지정된 포맷으로 반환합니다."""
    return datetime.now().strftime(format_string)

def format_duration(seconds):
    """초 단위 시간을 사람이 읽기 쉬운 형태로 변환합니다."""
    if seconds < 60:
        return f"{seconds:.1f}초"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}분"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}시간"

def time_since(start_time):
    """시작 시간부터 현재까지의 경과 시간을 반환합니다."""
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    
    elapsed = datetime.now() - start_time
    return elapsed.total_seconds()

class StopWatch:
    """간단한 스톱워치 클래스"""
    
    def __init__(self):
        self.start_time = None
        self.lap_times = []
    
    def start(self):
        """스톱워치를 시작합니다."""
        self.start_time = time.time()
        self.lap_times = []
        print("⏱️ 스톱워치 시작!")
    
    def lap(self):
        """랩 타임을 기록합니다."""
        if self.start_time is None:
            print("❌ 스톱워치가 시작되지 않았습니다.")
            return
        
        current_time = time.time()
        lap_time = current_time - self.start_time
        self.lap_times.append(lap_time)
        
        lap_number = len(self.lap_times)
        print(f"🏃 랩 {lap_number}: {format_duration(lap_time)}")
        return lap_time
    
    def stop(self):
        """스톱워치를 중지하고 총 시간을 반환합니다."""
        if self.start_time is None:
            print("❌ 스톱워치가 시작되지 않았습니다.")
            return 0
        
        total_time = time.time() - self.start_time
        print(f"🏁 총 시간: {format_duration(total_time)}")
        
        if self.lap_times:
            print(f"📊 총 {len(self.lap_times)}개 랩 기록됨")
        
        return total_time
''',
        "text_utils.py": '''
"""
텍스트 처리 유틸리티 함수들
"""

import re

def clean_text(text, remove_extra_spaces=True, remove_punctuation=False):
    """텍스트를 정리합니다."""
    # 앞뒤 공백 제거
    cleaned = text.strip()
    
    # 여러 공백을 하나로 변경
    if remove_extra_spaces:
        cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # 구두점 제거
    if remove_punctuation:
        cleaned = re.sub(r'[^\w\s]', '', cleaned)
    
    return cleaned

def extract_numbers(text):
    """텍스트에서 숫자들을 추출합니다."""
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return [float(num) if '.' in num else int(num) for num in numbers]

def extract_emails(text):
    """텍스트에서 이메일 주소들을 추출합니다."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

def word_count_detailed(text):
    """상세한 단어 통계를 반환합니다."""
    words = text.split()
    
    return {
        "total_words": len(words),
        "unique_words": len(set(word.lower() for word in words)),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "longest_word": max(words, key=len) if words else "",
        "shortest_word": min(words, key=len) if words else ""
    }

def generate_acronym(phrase):
    """구문에서 첫 글자들을 모아 약어를 만듭니다."""
    words = phrase.split()
    return ''.join(word[0].upper() for word in words if word)

class TextFormatter:
    """텍스트 포맷팅 도구"""
    
    @staticmethod
    def to_camel_case(text):
        """문자열을 camelCase로 변환합니다."""
        words = text.split()
        if not words:
            return ""
        
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    @staticmethod
    def to_snake_case(text):
        """문자열을 snake_case로 변환합니다."""
        return '_'.join(text.lower().split())
    
    @staticmethod
    def to_title_case(text):
        """문자열을 Title Case로 변환합니다."""
        return text.title()
    
    @staticmethod
    def add_line_numbers(text):
        """텍스트에 줄 번호를 추가합니다."""
        lines = text.split('\n')
        numbered_lines = [f"{i+1:3d}: {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered_lines)
''',
        "math_utils.py": '''
"""
수학 관련 유틸리티 함수들
"""

import math

def round_smart(number, precision=2):
    """스마트한 반올림 (불필요한 소수점 제거)"""
    rounded = round(number, precision)
    if rounded == int(rounded):
        return int(rounded)
    return rounded

def percentage(part, total, precision=1):
    """백분율을 계산합니다."""
    if total == 0:
        return 0
    return round_smart((part / total) * 100, precision)

def average(*numbers):
    """평균을 계산합니다."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def median(numbers):
    """중앙값을 계산합니다."""
    if not numbers:
        return 0
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    if n % 2 == 0:
        return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
        return sorted_numbers[n//2]

def standard_deviation(numbers):
    """표준편차를 계산합니다."""
    if len(numbers) < 2:
        return 0
    
    mean = average(*numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    return math.sqrt(variance)

def clamp(value, min_value, max_value):
    """값을 지정된 범위로 제한합니다."""
    return max(min_value, min(value, max_value))

def map_range(value, old_min, old_max, new_min, new_max):
    """값을 한 범위에서 다른 범위로 매핑합니다."""
    if old_max == old_min:
        return new_min
    
    ratio = (value - old_min) / (old_max - old_min)
    return new_min + ratio * (new_max - new_min)

class Statistics:
    """통계 계산 도구"""
    
    def __init__(self, data=None):
        self.data = data or []
    
    def add_data(self, *values):
        """데이터를 추가합니다."""
        self.data.extend(values)
    
    def clear_data(self):
        """데이터를 초기화합니다."""
        self.data = []
    
    def summary(self):
        """데이터 요약 통계를 반환합니다."""
        if not self.data:
            return {"error": "데이터가 없습니다"}
        
        return {
            "count": len(self.data),
            "sum": sum(self.data),
            "mean": average(*self.data),
            "median": median(self.data),
            "min": min(self.data),
            "max": max(self.data),
            "range": max(self.data) - min(self.data),
            "std_dev": standard_deviation(self.data)
        }
'''
    }
}

# personal_utils 패키지 생성
def create_package_structure(base_path, structure):
    """패키지 구조를 생성합니다."""
    for name, content in structure.items():
        current_path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # 디렉토리인 경우
            if not os.path.exists(current_path):
                os.makedirs(current_path)
            create_package_structure(current_path, content)
        else:
            # 파일인 경우
            with open(current_path, "w", encoding="utf-8") as f:
                f.write(content)

create_package_structure(".", personal_utils_structure)
print("✅ personal_utils 패키지가 생성되었습니다.")

# personal_utils 패키지 테스트
try:
    import personal_utils
    from personal_utils import time_utils, text_utils, math_utils
    
    print(f"\n개인 유틸리티 라이브러리 테스트:")
    print(f"버전: {personal_utils.__version__}")
    
    # 시간 유틸리티 테스트
    print(f"\n⏰ 시간 유틸리티:")
    print(f"현재 시간: {time_utils.get_current_time()}")
    print(f"3661초 포맷: {time_utils.format_duration(3661)}")
    
    # 텍스트 유틸리티 테스트
    print(f"\n📝 텍스트 유틸리티:")
    sample_text = "  Hello    World!!!  This is   a  test.  "
    cleaned = text_utils.clean_text(sample_text, remove_punctuation=True)
    print(f"원본: '{sample_text}'")
    print(f"정리됨: '{cleaned}'")
    
    numbers_text = "나이는 25살이고, 키는 175.5cm, 몸무게는 70kg입니다."
    numbers = text_utils.extract_numbers(numbers_text)
    print(f"숫자 추출: {numbers}")
    
    # 수학 유틸리티 테스트
    print(f"\n🔢 수학 유틸리티:")
    test_numbers = [85, 92, 78, 95, 88, 73, 91]
    
    stats = math_utils.Statistics(test_numbers)
    summary = stats.summary()
    
    print(f"데이터: {test_numbers}")
    print(f"평균: {summary['mean']:.1f}")
    print(f"중앙값: {summary['median']}")
    print(f"표준편차: {summary['std_dev']:.2f}")
    
    # 백분율 계산
    score = 85
    total = 100
    print(f"{score}/{total} = {math_utils.percentage(score, total)}%")

except ImportError as e:
    print(f"개인 유틸리티 패키지 import 오류: {e}")

print("\n=== 실습 예제 2: 웹 스크래핑 도구 패키지 ===")

# web_scraper 패키지 구조
web_scraper_structure = {
    "web_scraper": {
        "__init__.py": '''
"""
web_scraper - 웹 스크래핑 도구 패키지

웹 페이지에서 데이터를 추출하는 도구들을 제공합니다.
"""

__version__ = "0.2.0"

from .http_client import SimpleHTTPClient
from .html_parser import HTMLParser
from .data_extractor import extract_links, extract_text

# 패키지 설정
DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = "WebScraper/0.2.0"
''',
        "http_client.py": '''
"""
HTTP 클라이언트 모듈
"""

import urllib.request
import urllib.parse
import json
from urllib.error import URLError, HTTPError

class SimpleHTTPClient:
    """간단한 HTTP 클라이언트"""
    
    def __init__(self, timeout=10, user_agent="SimpleHTTPClient/1.0"):
        self.timeout = timeout
        self.user_agent = user_agent
    
    def get(self, url, headers=None):
        """GET 요청을 보냅니다."""
        try:
            request = urllib.request.Request(url)
            request.add_header('User-Agent', self.user_agent)
            
            if headers:
                for key, value in headers.items():
                    request.add_header(key, value)
            
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return {
                    "status_code": response.getcode(),
                    "content": response.read().decode('utf-8'),
                    "headers": dict(response.headers)
                }
        
        except HTTPError as e:
            return {"error": f"HTTP Error {e.code}: {e.reason}"}
        except URLError as e:
            return {"error": f"URL Error: {e.reason}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def download_file(self, url, filename):
        """파일을 다운로드합니다."""
        try:
            urllib.request.urlretrieve(url, filename)
            return {"success": True, "filename": filename}
        except Exception as e:
            return {"error": f"Download failed: {str(e)}"}
''',
        "html_parser.py": '''
"""
HTML 파싱 모듈
"""

import re

class HTMLParser:
    """간단한 HTML 파서"""
    
    def __init__(self, html_content):
        self.html = html_content
    
    def find_tags(self, tag_name):
        """특정 태그들을 찾습니다."""
        pattern = f'<{tag_name}[^>]*>(.*?)</{tag_name}>'
        matches = re.findall(pattern, self.html, re.DOTALL | re.IGNORECASE)
        return matches
    
    def find_tag_with_attrs(self, tag_name, **attrs):
        """속성을 가진 태그를 찾습니다."""
        # 간단한 속성 매칭 (정규식 기반)
        attr_pattern = ""
        for key, value in attrs.items():
            attr_pattern += f'[^>]*{key}=[\\'\\"]?{value}[\\'\\"]?'
        
        pattern = f'<{tag_name}{attr_pattern}[^>]*>(.*?)</{tag_name}>'
        matches = re.findall(pattern, self.html, re.DOTALL | re.IGNORECASE)
        return matches
    
    def extract_links(self):
        """모든 링크를 추출합니다."""
        pattern = r'<a[^>]*href=[\\'\\"]([^\\'\\"]*?)[\\'\\"][^>]*>(.*?)</a>'
        matches = re.findall(pattern, self.html, re.DOTALL | re.IGNORECASE)
        return [{"url": url, "text": self.clean_text(text)} for url, text in matches]
    
    def extract_images(self):
        """모든 이미지를 추출합니다."""
        pattern = r'<img[^>]*src=[\\'\\"]([^\\'\\"]*?)[\\'\\"][^>]*(?:alt=[\\'\\"]([^\\'\\"]*?)[\\'\\"])?[^>]*>'
        matches = re.findall(pattern, self.html, re.IGNORECASE)
        return [{"src": src, "alt": alt or ""} for src, alt in matches]
    
    def extract_text(self):
        """HTML에서 텍스트만 추출합니다."""
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', self.html)
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def clean_text(self, text):
        """텍스트를 정리합니다."""
        # HTML 엔티티 간단 처리
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
''',
        "data_extractor.py": '''
"""
데이터 추출 유틸리티 함수들
"""

import re
from .html_parser import HTMLParser

def extract_links(html_content, base_url=""):
    """HTML에서 링크들을 추출합니다."""
    parser = HTMLParser(html_content)
    links = parser.extract_links()
    
    # 상대 URL을 절대 URL로 변환
    if base_url:
        for link in links:
            if link["url"].startswith("/"):
                link["url"] = base_url.rstrip("/") + link["url"]
            elif not link["url"].startswith("http"):
                link["url"] = base_url.rstrip("/") + "/" + link["url"]
    
    return links

def extract_text(html_content):
    """HTML에서 텍스트만 추출합니다."""
    parser = HTMLParser(html_content)
    return parser.extract_text()

def extract_emails(text):
    """텍스트에서 이메일 주소들을 추출합니다."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

def extract_phone_numbers(text):
    """텍스트에서 전화번호들을 추출합니다."""
    patterns = [
        r'\d{3}-\d{4}-\d{4}',  # 010-1234-5678
        r'\d{2}-\d{3,4}-\d{4}',  # 02-123-4567
        r'\(\d{3}\)\s?\d{3}-\d{4}',  # (010) 123-4567
    ]
    
    phone_numbers = []
    for pattern in patterns:
        phone_numbers.extend(re.findall(pattern, text))
    
    return phone_numbers

def extract_table_data(html_content, table_index=0):
    """HTML 테이블에서 데이터를 추출합니다."""
    parser = HTMLParser(html_content)
    
    # 테이블 찾기
    table_pattern = r'<table[^>]*>(.*?)</table>'
    tables = re.findall(table_pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    if table_index >= len(tables):
        return []
    
    table_html = tables[table_index]
    
    # 행 찾기
    row_pattern = r'<tr[^>]*>(.*?)</tr>'
    rows = re.findall(row_pattern, table_html, re.DOTALL | re.IGNORECASE)
    
    table_data = []
    for row in rows:
        # 셀 찾기 (th 또는 td)
        cell_pattern = r'<(?:th|td)[^>]*>(.*?)</(?:th|td)>'
        cells = re.findall(cell_pattern, row, re.DOTALL | re.IGNORECASE)
        
        # 텍스트만 추출
        cell_texts = []
        for cell in cells:
            text_parser = HTMLParser(cell)
            cell_texts.append(text_parser.extract_text())
        
        if cell_texts:
            table_data.append(cell_texts)
    
    return table_data

class DataCleaner:
    """데이터 정리 도구"""
    
    @staticmethod
    def clean_whitespace(text):
        """공백 문자를 정리합니다."""
        return re.sub(r'\s+', ' ', text).strip()
    
    @staticmethod
    def remove_special_chars(text, keep_chars=""):
        """특수 문자를 제거합니다."""
        pattern = f'[^\\w\\s{re.escape(keep_chars)}]'
        return re.sub(pattern, '', text)
    
    @staticmethod
    def normalize_line_endings(text):
        """줄 바꿈 문자를 통일합니다."""
        return text.replace('\r\n', '\n').replace('\r', '\n')
    
    @staticmethod
    def extract_numbers(text):
        """텍스트에서 숫자를 추출합니다."""
        numbers = re.findall(r'-?\d+\.?\d*', text)
        return [float(num) if '.' in num else int(num) for num in numbers]
'''
    }
}

create_package_structure(".", web_scraper_structure)
print("✅ web_scraper 패키지가 생성되었습니다.")

# web_scraper 패키지 테스트
try:
    import web_scraper
    from web_scraper import http_client, html_parser, data_extractor
    
    print(f"\n웹 스크래퍼 패키지 테스트:")
    print(f"버전: {web_scraper.__version__}")
    
    # 간단한 HTML 파싱 테스트
    sample_html = '''
    <html>
    <head><title>테스트 페이지</title></head>
    <body>
        <h1>제목입니다</h1>
        <p>이것은 <a href="https://example.com">링크</a>가 있는 문단입니다.</p>
        <p>연락처: test@example.com, 전화: 010-1234-5678</p>
        <img src="image.jpg" alt="테스트 이미지">
        <table>
            <tr><th>이름</th><th>나이</th></tr>
            <tr><td>김철수</td><td>25</td></tr>
            <tr><td>이영희</td><td>30</td></tr>
        </table>
    </body>
    </html>
    '''
    
    # HTML 파서 테스트
    parser = html_parser.HTMLParser(sample_html)
    
    print(f"\n🔍 HTML 파싱 결과:")
    print(f"제목들: {parser.find_tags('h1')}")
    
    links = parser.extract_links()
    print(f"링크들: {[link['url'] for link in links]}")
    
    # 데이터 추출 테스트
    text = data_extractor.extract_text(sample_html)
    print(f"추출된 텍스트: {text[:50]}...")
    
    emails = data_extractor.extract_emails(text)
    print(f"이메일들: {emails}")
    
    phones = data_extractor.extract_phone_numbers(text)
    print(f"전화번호들: {phones}")
    
    table_data = data_extractor.extract_table_data(sample_html)
    print(f"테이블 데이터:")
    for row in table_data:
        print(f"  {row}")

except ImportError as e:
    print(f"웹 스크래퍼 패키지 import 오류: {e}")

# ===================================================================
# 8. 모듈과 패키지 관리 모범 사례
# ===================================================================

print("\n=== 모듈과 패키지 관리 모범 사례 ===")

best_practices = """
📋 모듈과 패키지 관리 모범 사례:

1. 📁 패키지 구조 설계:
   - 논리적으로 관련된 기능들을 그룹화
   - 패키지 이름은 소문자와 언더스코어 사용
   - __init__.py 파일로 패키지 초기화

2. 📝 문서화:
   - 각 모듈과 함수에 docstring 작성
   - README.md 파일로 사용법 설명
   - 타입 힌트 사용 (Python 3.5+)

3. 🔄 버전 관리:
   - 시맨틱 버저닝 사용 (예: 1.2.3)
   - CHANGELOG.md로 변경사항 기록
   - __version__ 변수로 버전 정보 제공

4. 🧪 테스트:
   - 각 모듈에 대한 단위 테스트 작성
   - tests/ 디렉토리에 테스트 파일 구성
   - pytest, unittest 등 테스트 프레임워크 활용

5. 📦 의존성 관리:
   - requirements.txt 또는 pyproject.toml 사용
   - 가상환경에서 개발
   - 버전 범위 명시 (예: requests>=2.25.0,<3.0.0)

6. 🚀 배포:
   - setup.py 또는 pyproject.toml로 패키지 설정
   - PyPI에 업로드하여 pip install 가능하게 만들기
   - CI/CD 파이프라인 구축

7. 🔒 보안:
   - 민감한 정보는 환경 변수 사용
   - .gitignore로 불필요한 파일 제외
   - 의존성 보안 취약점 정기 점검
"""

print(best_practices)

# setup.py 예제 파일 생성
setup_py_content = '''
"""
setup.py - 패키지 설치 설정 파일

이 파일은 패키지를 PyPI에 업로드하거나 pip install로 설치할 때 사용됩니다.
"""

from setuptools import setup, find_packages

# README 파일 읽기
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# requirements.txt 읽기
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mypackage",
    version="1.0.0",
    author="파이썬 학습자",
    author_email="learner@example.com",
    description="파이썬 학습용 예제 패키지",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/mypackage",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mypackage-cli=mypackage.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
'''

with open("setup.py", "w", encoding="utf-8") as f:
    f.write(setup_py_content)

# README.md 예제 생성
readme_content = '''# MyPackage

파이썬 학습용 예제 패키지입니다.

## 설치

```bash
pip install mypackage
```

## 사용법

### 기본 사용법

```python
import mypackage
from mypackage.math_tools import add, multiply

# 기본 연산
result = add(10, 5)
print(f"10 + 5 = {result}")

# 패키지 정보
print(f"버전: {mypackage.__version__}")
```

### 고급 사용법

```python
from mypackage.math_tools.advanced import factorial, fibonacci
from mypackage.string_tools import reverse_string, count_words

# 고급 수학 함수
print(f"5! = {factorial(5)}")
print(f"10번째 피보나치: {fibonacci(10)}")

# 문자열 처리
text = "Hello Python World"
print(f"뒤집기: {reverse_string(text)}")
print(f"단어 수: {count_words(text)}")
```

## 패키지 구조

```
mypackage/
├── __init__.py
├── math_tools/
│   ├── __init__.py
│   ├── basic.py
│   └── advanced.py
├── string_tools/
│   ├── __init__.py
│   ├── text.py
│   └── validation.py
└── file_tools/
    ├── __init__.py
    ├── file_operations.py
    └── file_info.py
```

## 개발

### 개발 환경 설정

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\\Scripts\\activate   # Windows

# 개발용 의존성 설치
pip install -e .[dev]
```

### 테스트 실행

```bash
pytest tests/
```

### 코드 포맷팅

```bash
black mypackage/
```

## 라이선스

MIT License

## 기여

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 변경사항

자세한 변경사항은 [CHANGELOG.md](CHANGELOG.md)를 참조하세요.
'''

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("✅ setup.py와 README.md 파일이 생성되었습니다.")

# ===================================================================
# 9. 실제 사용 시나리오들
# ===================================================================

print("\n=== 실제 사용 시나리오들 ===")

def scenario_data_processing():
    """시나리오 1: 데이터 처리 프로젝트"""
    print("📊 데이터 처리 프로젝트 패키지 구조:")
    
    data_project_structure = """
data_processor/
├── __init__.py
├── readers/
│   ├── __init__.py
│   ├── csv_reader.py
│   ├── json_reader.py
│   └── excel_reader.py
├── cleaners/
│   ├── __init__.py
│   ├── text_cleaner.py
│   ├── numeric_cleaner.py
│   └── date_cleaner.py
├── analyzers/
│   ├── __init__.py
│   ├── statistics.py
│   ├── trends.py
│   └── correlations.py
├── exporters/
│   ├── __init__.py
│   ├── report_generator.py
│   └── visualization.py
└── utils/
    ├── __init__.py
    ├── logging.py
    └── config.py
    """
    
    print(data_project_structure)
    
    usage_example = '''
# 사용 예제
from data_processor.readers import csv_reader
from data_processor.cleaners import text_cleaner
from data_processor.analyzers import statistics
from data_processor.exporters import report_generator

# 데이터 처리 파이프라인
data = csv_reader.load("sales_data.csv")
cleaned_data = text_cleaner.clean_text_columns(data)
stats = statistics.calculate_summary(cleaned_data)
report_generator.create_pdf_report(stats, "sales_report.pdf")
'''
    
    print("사용 예제:")
    print(usage_example)

def scenario_web_application():
    """시나리오 2: 웹 애플리케이션 프로젝트"""
    print("\n🌐 웹 애플리케이션 프로젝트 패키지 구조:")
    
    web_project_structure = """
webapp/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   └── order.py
├── views/
│   ├── __init__.py
│   ├── auth_views.py
│   ├── product_views.py
│   └── order_views.py
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   └── product_controller.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── migrations.py
├── templates/
│   ├── base.html
│   ├── login.html
│   └── products.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── utils/
    ├── __init__.py
    ├── validators.py
    └── helpers.py
    """
    
    print(web_project_structure)

def scenario_machine_learning():
    """시나리오 3: 머신러닝 프로젝트"""
    print("\n🤖 머신러닝 프로젝트 패키지 구조:")
    
    ml_project_structure = """
ml_toolkit/
├── __init__.py
├── data/
│   ├── __init__.py
│   ├── loaders.py
│   ├── preprocessors.py
│   └── validators.py
├── features/
│   ├── __init__.py
│   ├── extractors.py
│   ├── selectors.py
│   └── transformers.py
├── models/
│   ├── __init__.py
│   ├── regression.py
│   ├── classification.py
│   └── clustering.py
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py
│   └── cross_validation.py
├── visualization/
│   ├── __init__.py
│   ├── plots.py
│   └── reports.py
└── utils/
    ├── __init__.py
    ├── math_utils.py
    └── io_utils.py
    """
    
    print(ml_project_structure)

# 시나리오들 실행
scenario_data_processing()
scenario_web_application()
scenario_machine_learning()

# ===================================================================
# 10. 마무리 및 실습 과제
# ===================================================================

print("\n=== 실습 과제 ===")

assignments = """
🎯 모듈과 패키지 실습 과제:

과제 1: 개인 도구 패키지 만들기
- 자주 사용하는 함수들을 모아서 패키지 제작
- 최소 3개 서브패키지 구성
- __init__.py에 주요 함수들을 패키지 레벨에서 import 가능하게 설정
- docstring으로 문서화

과제 2: 특정 도메인 전용 패키지
- 선택한 도메인(게임, 금융, 교육 등)에 특화된 패키지 제작
- 실제 사용 가능한 기능들 구현
- 예외 처리와 입력 검증 포함
- 테스트 코드 작성

과제 3: 기존 패키지 확장
- 표준 라이브러리나 유명한 패키지를 확장하는 래퍼 패키지 제작
- 더 편리한 인터페이스 제공
- 추가 기능 구현
- 사용 예제와 문서 작성

과제 4: CLI 도구 패키지
- 명령행에서 사용할 수 있는 도구 제작
- argparse를 사용한 명령행 인터페이스
- setup.py의 entry_points 활용
- 파일 처리, 데이터 변환 등 실용적 기능

과제 5: 패키지 배포 연습
- 완성된 패키지를 setup.py로 설치 가능하게 만들기
- requirements.txt 작성
- README.md와 문서 작성
- (선택사항) 테스트용 PyPI에 업로드해보기
"""

print(assignments)

print("\n=== 12단계 완료! ===")
print("모듈과 패키지를 모두 배웠습니다.")
print("이제 파이썬의 모든 기초를 마스터했습니다! 🎉")

# 학습 완료 통계
completion_stats = """
🎓 파이썬 기초 과정 완료!

학습한 내용:
✅ 1단계: 프로그래밍 기초 개념
✅ 2단계: 기본 데이터 타입과 변수  
✅ 3단계: 기본 연산자
✅ 4단계: 입출력
✅ 5단계: 조건문
✅ 6단계: 반복문
✅ 7단계: 데이터 구조 (리스트, 딕셔너리, 집합, 튜플)
✅ 8단계: 문자열 심화
✅ 9단계: 함수
✅ 10단계: 예외 처리
✅ 11단계: 파일 입출력
✅ 12단계: 모듈과 패키지

🚀 다음 단계 추천:
- 객체 지향 프로그래밍 (클래스와 객체)
- 고급 파이썬 기법 (데코레이터, 제너레이터, 컨텍스트 매니저)
- 웹 개발 (Flask, Django)
- 데이터 사이언스 (NumPy, Pandas, Matplotlib)
- 머신러닝 (Scikit-learn, TensorFlow, PyTorch)
- 웹 스크래핑 (BeautifulSoup, Selenium)
- API 개발 (FastAPI, REST API)
- 테스트 주도 개발 (pytest, unittest)
- 배포와 DevOps (Docker, CI/CD)

축하합니다! 🎉
"""

print(completion_stats)

# ===================================================================
# 추가 팁
# ===================================================================

"""
12단계에서 기억해야 할 중요한 점들:

1. 모듈 import 방식:
   - import module
   - from module import function
   - import module as alias
   - from module import *  (권장하지 않음)

2. 패키지 구조:
   - __init__.py 파일로 패키지 정의
   - 논리적 계층 구조 설계
   - 관련 기능들을 그룹화

3. 모듈 검색 경로:
   - sys.path에 포함된 경로에서 모듈 검색
   - PYTHONPATH 환경 변수 활용
   - 현재 디렉토리가 기본 포함

4. 패키지 배포:
   - setup.py로 설치 가능한 패키지 제작
   - requirements.txt로 의존성 관리
   - PyPI 업로드로 전 세계 공유

5. 모범 사례:
   - 명확한 패키지 구조
   - 충분한 문서화 (docstring, README)
   - 테스트 코드 작성
   - 버전 관리

6. 가상환경 사용:
   - 프로젝트별 독립적인 환경 구성
   - python -m venv 명령어 활용
   - requirements.txt로 환경 재현

실습할 때 꼭 해보세요:
- 자주 사용하는 함수들을 모듈로 만들어보기
- 관련 모듈들을 패키지로 그룹화하기
- 표준 라이브러리 다양하게 활용해보기
- 실제 프로젝트에서 패키지 구조 설계하기
- pip로 외부 패키지 설치하고 사용해보기
"""
