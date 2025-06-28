# ===================================================================
# 파이썬 8단계: 문자열 심화 실습 코드
# ===================================================================

# ===================================================================
# 1. 문자열 메서드 완전 정복
# ===================================================================

print("=== 문자열 메서드 기초 ===")

# 대소문자 변환
text = "Hello Python World"
print(f"원본: {text}")
print(f"대문자: {text.upper()}")
print(f"소문자: {text.lower()}")
print(f"첫 글자만 대문자: {text.capitalize()}")
print(f"각 단어 첫 글자 대문자: {text.title()}")
print(f"대소문자 바꾸기: {text.swapcase()}")

# 문자열 검사
print(f"\n=== 문자열 검사 메서드 ===")
test_strings = ["Hello123", "12345", "Hello", "hello world", "   ", ""]

for s in test_strings:
    print(f"'{s}':")
    print(f"  알파벳인가? {s.isalpha()}")
    print(f"  숫자인가? {s.isdigit()}")
    print(f"  알파벳+숫자인가? {s.isalnum()}")
    print(f"  공백인가? {s.isspace()}")
    print(f"  대문자인가? {s.isupper()}")
    print(f"  소문자인가? {s.islower()}")
    print(f"  제목 형식인가? {s.istitle()}")
    print()

print("=== 문자열 검색과 위치 ===")

text = "Python is great. Python is powerful. Python is fun."
print(f"텍스트: {text}")

# find() vs index()
search_word = "Python"
print(f"'{search_word}' 첫 번째 위치: {text.find(search_word)}")
print(f"'{search_word}' 마지막 위치: {text.rfind(search_word)}")
print(f"'{search_word}' 개수: {text.count(search_word)}")

# 포함 여부 확인
print(f"'great'가 포함되어 있나? {'great' in text}")
print(f"'awesome'이 포함되어 있나? {'awesome' in text}")

# 시작/끝 확인
print(f"'Python'으로 시작하나? {text.startswith('Python')}")
print(f"'fun.'으로 끝나나? {text.endswith('fun.')}")

print("\n=== 문자열 분할과 결합 ===")

# split() - 문자열 분할
sentence = "apple,banana,orange,grape"
fruits = sentence.split(",")
print(f"쉼표로 분할: {fruits}")

paragraph = "첫 번째 줄\n두 번째 줄\n세 번째 줄"
lines = paragraph.split("\n")
print(f"줄 단위로 분할: {lines}")

# 공백으로 분할 (기본값)
words = "  hello   world   python  ".split()
print(f"공백으로 분할: {words}")

# 분할 횟수 제한
text = "a-b-c-d-e"
parts = text.split("-", 2)  # 최대 2번만 분할
print(f"제한된 분할: {parts}")

# join() - 문자열 결합
words = ["Python", "is", "awesome"]
sentence = " ".join(words)
print(f"공백으로 결합: {sentence}")

sentence = "-".join(words)
print(f"하이픈으로 결합: {sentence}")

# 숫자 리스트도 결합 가능 (문자열로 변환 후)
numbers = [1, 2, 3, 4, 5]
number_string = ",".join(map(str, numbers))
print(f"숫자를 문자열로 결합: {number_string}")

print("\n=== 문자열 치환과 제거 ===")

# replace() - 문자열 치환
text = "I love Java. Java is great. Java is powerful."
print(f"원본: {text}")

# 모든 'Java'를 'Python'으로 치환
new_text = text.replace("Java", "Python")
print(f"치환 후: {new_text}")

# 처음 2개만 치환
limited_replace = text.replace("Java", "Python", 2)
print(f"제한 치환: {limited_replace}")

# 공백과 특수문자 제거
messy_text = "   Hello World!   "
print(f"원본: '{messy_text}'")
print(f"양쪽 공백 제거: '{messy_text.strip()}'")
print(f"왼쪽 공백 제거: '{messy_text.lstrip()}'")
print(f"오른쪽 공백 제거: '{messy_text.rstrip()}'")

# 특정 문자 제거
text_with_punctuation = "!!!Hello World!!!"
print(f"느낌표 제거: '{text_with_punctuation.strip('!')}'")

# ===================================================================
# 2. 문자열 인덱싱과 슬라이싱 심화
# ===================================================================

print("\n=== 문자열 인덱싱과 슬라이싱 심화 ===")

text = "Python Programming"
print(f"문자열: {text}")
print(f"길이: {len(text)}")

# 기본 인덱싱
print(f"첫 번째 문자: {text[0]}")
print(f"마지막 문자: {text[-1]}")
print(f"뒤에서 두 번째: {text[-2]}")

# 슬라이싱 패턴들
print(f"처음 6글자: {text[:6]}")  # Python
print(f"7번째부터 끝까지: {text[7:]}")  # Programming
print(f"3번째부터 8번째까지: {text[3:9]}")  # hon Pr
print(f"2칸씩 건너뛰기: {text[::2]}")  # Pto rgamn
print(f"거꾸로: {text[::-1]}")  # gnimmargorP nohtyP

# 실용적인 슬라이싱 예제
email = "user@example.com"
username = email[:email.find("@")]
domain = email[email.find("@")+1:]
print(f"이메일: {email}")
print(f"사용자명: {username}")
print(f"도메인: {domain}")

# 파일 확장자 추출
filename = "document.pdf"
name = filename[:filename.rfind(".")]
extension = filename[filename.rfind(".")+1:]
print(f"파일명: {filename}")
print(f"이름: {name}")
print(f"확장자: {extension}")

# ===================================================================
# 3. 문자열 포매팅 완전 정복
# ===================================================================

print("\n=== 문자열 포매팅 심화 ===")

# f-string 고급 기능
name = "김파이썬"
age = 25
score = 85.67892
price = 1234567

print("=== f-string 고급 포매팅 ===")
print(f"기본: {name}님의 나이는 {age}세입니다.")

# 정렬과 폭 지정
print(f"왼쪽 정렬: '{name:<10}'")
print(f"오른쪽 정렬: '{name:>10}'")
print(f"가운데 정렬: '{name:^10}'")

# 숫자 포매팅
print(f"소수점 2자리: {score:.2f}")
print(f"소수점 없음: {score:.0f}")
print(f"천 단위 구분: {price:,}")
print(f"천 단위 + 소수점: {score:,.2f}")

# 진법 변환
number = 255
print(f"10진수: {number}")
print(f"2진수: {number:b}")
print(f"8진수: {number:o}")
print(f"16진수: {number:x}")
print(f"16진수(대문자): {number:X}")

# 퍼센트 표시
ratio = 0.856
print(f"비율: {ratio:.1%}")

# 패딩과 채우기
print(f"0으로 패딩: {age:05d}")  # 5자리로 만들고 앞에 0 채우기
print(f"*로 채우기: {name:*^15}")

# 날짜와 시간 포매팅 예제
year, month, day = 2025, 6, 28
hour, minute = 14, 30

print(f"날짜: {year}-{month:02d}-{day:02d}")
print(f"시간: {hour:02d}:{minute:02d}")

print("\n=== .format() 메서드 ===")

# 위치 인수
template = "이름: {}, 나이: {}, 점수: {:.1f}"
result = template.format(name, age, score)
print(result)

# 인덱스 지정
template = "나이: {1}, 이름: {0}, 점수: {2:.1f}"
result = template.format(name, age, score)
print(result)

# 키워드 인수
template = "이름: {name}, 나이: {age}, 점수: {score:.1f}"
result = template.format(name=name, age=age, score=score)
print(result)

# ===================================================================
# 4. 정규표현식 기초
# ===================================================================

print("\n=== 정규표현식 기초 ===")

import re

# 기본 패턴 매칭
text = "제 전화번호는 010-1234-5678이고, 집 전화는 02-123-4567입니다."
print(f"텍스트: {text}")

# 휴대폰 번호 찾기
phone_pattern = r"010-\d{4}-\d{4}"
mobile_phones = re.findall(phone_pattern, text)
print(f"휴대폰 번호: {mobile_phones}")

# 모든 전화번호 찾기
all_phone_pattern = r"\d{2,3}-\d{3,4}-\d{4}"
all_phones = re.findall(all_phone_pattern, text)
print(f"모든 전화번호: {all_phones}")

# 이메일 검증
emails = ["test@example.com", "invalid.email", "user123@domain.co.kr", "bad@", "@domain.com"]
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

print("\n이메일 유효성 검사:")
for email in emails:
    is_valid = bool(re.match(email_pattern, email))
    print(f"{email}: {'유효' if is_valid else '무효'}")

# 문자열 치환 (정규표현식 사용)
text_with_numbers = "가격은 1,234,567원이고, 할인가는 987,654원입니다."
print(f"원본: {text_with_numbers}")

# 숫자에서 쉼표 제거
no_comma = re.sub(r",", "", text_with_numbers)
print(f"쉼표 제거: {no_comma}")

# 숫자만 추출
numbers_only = re.findall(r"\d+", text_with_numbers)
print(f"숫자만 추출: {numbers_only}")

# ===================================================================
# 5. 실습 예제들
# ===================================================================

print("\n=== 실습 예제 1: 텍스트 분석기 ===")

def analyze_text(text):
    """텍스트를 분석하여 다양한 통계를 반환하는 함수"""
    
    # 기본 통계
    char_count = len(text)
    char_count_no_space = len(text.replace(" ", ""))
    word_count = len(text.split())
    sentence_count = text.count(".") + text.count("!") + text.count("?")
    
    # 단어 빈도
    words = text.lower().split()
    word_freq = {}
    for word in words:
        # 구두점 제거
        clean_word = word.strip(".,!?;:")
        if clean_word:
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    # 가장 빈번한 단어 찾기
    if word_freq:
        most_common_word = max(word_freq, key=word_freq.get)
        most_common_count = word_freq[most_common_word]
    else:
        most_common_word = "없음"
        most_common_count = 0
    
    # 결과 출력
    print("=== 텍스트 분석 결과 ===")
    print(f"총 문자 수: {char_count}개")
    print(f"공백 제외 문자 수: {char_count_no_space}개")
    print(f"단어 수: {word_count}개")
    print(f"문장 수: {sentence_count}개")
    print(f"가장 빈번한 단어: '{most_common_word}' ({most_common_count}회)")
    
    print(f"\n단어 빈도 (상위 5개):")
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:5]:
        print(f"  {word}: {count}회")
    
    return {
        "char_count": char_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "word_frequency": word_freq
    }

# 테스트 텍스트
sample_text = """
파이썬은 강력하고 사용하기 쉬운 프로그래밍 언어입니다. 
파이썬은 다양한 분야에서 사용됩니다. 
웹 개발, 데이터 분석, 인공지능 등 많은 분야에서 파이썬이 활용됩니다.
파이썬을 배우면 많은 것을 할 수 있습니다!
"""

analyze_text(sample_text.strip())

print("\n=== 실습 예제 2: 비밀번호 검증기 ===")

def validate_password(password):
    """비밀번호 강도를 검증하는 함수"""
    
    conditions = {
        "길이 8자 이상": len(password) >= 8,
        "대문자 포함": any(c.isupper() for c in password),
        "소문자 포함": any(c.islower() for c in password),
        "숫자 포함": any(c.isdigit() for c in password),
        "특수문자 포함": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    }
    
    # 통과한 조건 수
    passed_conditions = sum(conditions.values())
    
    # 강도 계산
    if passed_conditions <= 2:
        strength = "매우 약함"
    elif passed_conditions == 3:
        strength = "약함"
    elif passed_conditions == 4:
        strength = "보통"
    else:
        strength = "강함"
    
    print(f"비밀번호: {password}")
    print(f"강도: {strength} ({passed_conditions}/5)")
    
    for condition, passed in conditions.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {condition}")
    
    return passed_conditions >= 4  # 4개 이상 조건 만족시 유효

# 비밀번호 테스트
test_passwords = [
    "123456",
    "password",
    "Password123",
    "MyP@ssw0rd",
    "VeryStr0ng!P@ssw0rd"
]

print("비밀번호 강도 검사:")
for pwd in test_passwords:
    print()
    is_valid = validate_password(pwd)
    print(f"유효성: {'통과' if is_valid else '실패'}")
    print("-" * 30)

print("\n=== 실습 예제 3: 문자열 암호화/복호화 ===")

def caesar_cipher(text, shift, mode="encrypt"):
    """시저 암호 구현"""
    result = ""
    
    # 복호화시 shift 방향 반대
    if mode == "decrypt":
        shift = -shift
    
    for char in text:
        if char.isalpha():
            # 대문자 처리
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            # 소문자 처리
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            # 알파벳이 아닌 문자는 그대로
            result += char
    
    return result

# 시저 암호 테스트
original_text = "Hello World! Python is Great."
shift_value = 3

print(f"원본 텍스트: {original_text}")

encrypted = caesar_cipher(original_text, shift_value, "encrypt")
print(f"암호화된 텍스트: {encrypted}")

decrypted = caesar_cipher(encrypted, shift_value, "decrypt")
print(f"복호화된 텍스트: {decrypted}")

print(f"복호화 성공: {original_text == decrypted}")

print("\n=== 실습 예제 4: 파일명 정리기 ===")

def clean_filename(filename):
    """파일명을 안전한 형태로 정리하는 함수"""
    
    # 금지된 문자들
    forbidden_chars = '<>:"/\\|?*'
    
    # 원본 파일명 정보
    print(f"원본 파일명: '{filename}'")
    
    # 1. 금지된 문자 제거
    clean_name = filename
    for char in forbidden_chars:
        clean_name = clean_name.replace(char, "_")
    
    # 2. 연속된 공백을 하나로
    clean_name = re.sub(r"\s+", " ", clean_name)
    
    # 3. 앞뒤 공백 제거
    clean_name = clean_name.strip()
    
    # 4. 빈 파일명 처리
    if not clean_name:
        clean_name = "untitled"
    
    # 5. 너무 긴 파일명 처리 (확장자 고려)
    if "." in clean_name:
        name_part, ext = clean_name.rsplit(".", 1)
        if len(name_part) > 200:
            name_part = name_part[:200]
        clean_name = f"{name_part}.{ext}"
    else:
        if len(clean_name) > 200:
            clean_name = clean_name[:200]
    
    print(f"정리된 파일명: '{clean_name}'")
    
    # 변경사항 요약
    changes = []
    if filename != clean_name:
        changes.append("파일명이 수정되었습니다")
        if any(char in filename for char in forbidden_chars):
            changes.append("금지된 문자가 '_'로 변경됨")
        if "  " in filename:
            changes.append("연속된 공백이 정리됨")
        if filename.strip() != filename:
            changes.append("앞뒤 공백이 제거됨")
    
    if changes:
        print("변경사항:", ", ".join(changes))
    else:
        print("변경사항: 없음")
    
    return clean_name

# 파일명 정리 테스트
problematic_filenames = [
    "my<file>name.txt",
    "document   with   spaces.pdf",
    "   file with leading spaces.doc",
    "file/with\\forbidden:chars.xlsx",
    "normal_filename.jpg",
    "",
    "very_long_filename_that_exceeds_normal_limits_and_should_be_truncated_somehow.txt"
]

print("파일명 정리 테스트:")
for filename in problematic_filenames:
    print()
    clean_filename(filename)
    print("-" * 40)

print("\n=== 실습 예제 5: 스마트 검색 시스템 ===")

def smart_search(query, text_list, case_sensitive=False):
    """스마트 검색 시스템 - 부분 일치, 유사도 등을 고려"""
    
    if not case_sensitive:
        query = query.lower()
    
    results = {
        "exact_match": [],      # 정확한 일치
        "starts_with": [],      # 시작 부분 일치
        "contains": [],         # 포함
        "word_match": []        # 단어 단위 일치
    }
    
    for i, text in enumerate(text_list):
        search_text = text if case_sensitive else text.lower()
        
        if query == search_text:
            results["exact_match"].append((i, text))
        elif search_text.startswith(query):
            results["starts_with"].append((i, text))
        elif query in search_text:
            results["contains"].append((i, text))
        elif query in search_text.split():
            results["word_match"].append((i, text))
    
    return results

# 검색 테스트
documents = [
    "Python 프로그래밍 기초",
    "파이썬으로 배우는 데이터 분석",
    "JavaScript 완벽 가이드",
    "파이썬 웹 개발",
    "데이터 사이언스와 Python",
    "자바스크립트 기초부터 고급까지",
    "Python으로 만드는 인공지능",
    "프로그래밍 언어 Python 3"
]

search_queries = ["python", "파이썬", "javascript"]

for query in search_queries:
    print(f"\n검색어: '{query}'")
    print("=" * 30)
    
    search_results = smart_search(query, documents)
    
    for category, matches in search_results.items():
        if matches:
            category_names = {
                "exact_match": "정확한 일치",
                "starts_with": "시작 부분 일치", 
                "contains": "포함",
                "word_match": "단어 일치"
            }
            print(f"\n{category_names[category]}:")
            for index, text in matches:
                print(f"  [{index}] {text}")

print("\n=== 8단계 완료! ===")
print("문자열 심화 과정을 모두 배웠습니다.")
print("다음 단계에서는 함수를 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
8단계에서 기억해야 할 중요한 점들:

1. 문자열 메서드:
   - 대소문자: upper(), lower(), capitalize(), title()
   - 검사: isalpha(), isdigit(), isalnum(), isspace()
   - 검색: find(), index(), count(), startswith(), endswith()
   - 분할/결합: split(), join()
   - 치환/제거: replace(), strip(), lstrip(), rstrip()

2. 인덱싱과 슬라이싱:
   - text[start:end:step]
   - 음수 인덱스 활용
   - 거꾸로 뒤집기: text[::-1]

3. 문자열 포매팅:
   - f-string (권장): f"{변수:포맷}"
   - .format() 메서드
   - 다양한 포맷 옵션: 정렬, 소수점, 천단위 구분 등

4. 정규표현식 기초:
   - import re
   - 패턴 매칭: re.findall(), re.match(), re.search()
   - 치환: re.sub()

5. 실무 활용:
   - 데이터 검증 (이메일, 전화번호, 비밀번호)
   - 텍스트 분석 (단어 빈도, 통계)
   - 파일명 정리
   - 검색 시스템

실습할 때 꼭 해보세요:
- 다양한 문자열 메서드 조합해서 사용하기
- 정규표현식으로 패턴 찾기
- f-string으로 예쁜 출력 만들기
- 실제 텍스트 처리 문제 해결하기
"""
