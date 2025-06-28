# ===================================================================
# 파이썬 7단계: 데이터 구조 실습 코드
# ===================================================================

# ===================================================================
# 1. 리스트 (List) - 순서가 있는 변경 가능한 데이터 집합
# ===================================================================

print("=== 리스트 기초 ===")

# 리스트 생성
fruits = ["사과", "바나나", "오렌지"]
numbers = [1, 2, 3, 4, 5]
mixed_list = ["파이썬", 3.14, 42, True]
empty_list = []

print("과일 리스트:", fruits)
print("숫자 리스트:", numbers)
print("혼합 리스트:", mixed_list)
print("빈 리스트:", empty_list)

# 리스트 길이
print(f"과일 개수: {len(fruits)}개")

print("\n=== 리스트 인덱싱과 슬라이싱 ===")

# 인덱싱 (0부터 시작)
print(f"첫 번째 과일: {fruits[0]}")
print(f"두 번째 과일: {fruits[1]}")
print(f"마지막 과일: {fruits[-1]}")  # 음수 인덱스
print(f"뒤에서 두 번째: {fruits[-2]}")

# 슬라이싱 [start:end:step]
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"전체: {numbers}")
print(f"처음 3개: {numbers[:3]}")     # [0, 1, 2]
print(f"3번째부터: {numbers[3:]}")    # [3, 4, 5, 6, 7, 8, 9]
print(f"2번째~5번째: {numbers[2:6]}")  # [2, 3, 4, 5]
print(f"짝수 인덱스: {numbers[::2]}")   # [0, 2, 4, 6, 8]
print(f"거꾸로: {numbers[::-1]}")      # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

print("\n=== 리스트 수정 ===")

# 요소 변경
fruits = ["사과", "바나나", "오렌지"]
print("원본:", fruits)

fruits[1] = "포도"  # 바나나를 포도로 변경
print("변경 후:", fruits)

# 슬라이싱으로 여러 요소 변경
numbers = [1, 2, 3, 4, 5]
numbers[1:4] = [20, 30, 40]
print("슬라이싱 변경:", numbers)

print("\n=== 리스트 메서드 ===")

# append() - 끝에 요소 추가
shopping_list = ["우유", "빵"]
print("초기 리스트:", shopping_list)

shopping_list.append("계란")
shopping_list.append("치즈")
print("추가 후:", shopping_list)

# insert() - 특정 위치에 삽입
shopping_list.insert(1, "버터")  # 1번 인덱스에 삽입
print("삽입 후:", shopping_list)

# extend() - 다른 리스트 전체 추가
more_items = ["사과", "바나나"]
shopping_list.extend(more_items)
print("확장 후:", shopping_list)

# remove() - 값으로 제거 (첫 번째 발견되는 것만)
shopping_list.remove("빵")
print("빵 제거 후:", shopping_list)

# pop() - 인덱스로 제거하고 반환
removed_item = shopping_list.pop()  # 마지막 요소 제거
print(f"제거된 항목: {removed_item}")
print("pop 후:", shopping_list)

removed_item = shopping_list.pop(0)  # 첫 번째 요소 제거
print(f"제거된 항목: {removed_item}")
print("첫 번째 제거 후:", shopping_list)

# index() - 값의 인덱스 찾기
fruits = ["사과", "바나나", "오렌지", "바나나"]
print(f"바나나의 위치: {fruits.index('바나나')}")  # 첫 번째 바나나

# count() - 값의 개수 세기
print(f"바나나 개수: {fruits.count('바나나')}")

# sort() - 정렬 (원본 변경)
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print("정렬 전:", numbers)
numbers.sort()
print("오름차순:", numbers)
numbers.sort(reverse=True)
print("내림차순:", numbers)

# sorted() - 정렬된 새 리스트 반환 (원본 유지)
original = [3, 1, 4, 1, 5]
sorted_list = sorted(original)
print("원본:", original)
print("정렬된 복사본:", sorted_list)

# reverse() - 순서 뒤집기
fruits = ["사과", "바나나", "오렌지"]
fruits.reverse()
print("뒤집힌 리스트:", fruits)

print("\n=== 리스트 실습 예제 ===")

# 학생 성적 관리
students = []
grades = []

# 학생 추가
student_data = [
    ("김철수", 85),
    ("이영희", 92),
    ("박민수", 78),
    ("최영수", 95),
    ("한지민", 88)
]

for name, grade in student_data:
    students.append(name)
    grades.append(grade)

print("학생 명단:", students)
print("성적 리스트:", grades)

# 통계 계산
total_score = sum(grades)
average_score = total_score / len(grades)
highest_score = max(grades)
lowest_score = min(grades)

print(f"총점: {total_score}")
print(f"평균: {average_score:.1f}")
print(f"최고점: {highest_score}")
print(f"최저점: {lowest_score}")

# 성적 순으로 정렬 (학생명과 함께)
student_grade_pairs = list(zip(students, grades))
student_grade_pairs.sort(key=lambda x: x[1], reverse=True)  # 성적 기준 내림차순

print("\n성적순 순위:")
for i, (name, grade) in enumerate(student_grade_pairs, 1):
    print(f"{i}등: {name} ({grade}점)")

# ===================================================================
# 2. 튜플 (Tuple) - 순서가 있는 변경 불가능한 데이터 집합
# ===================================================================

print("\n=== 튜플 기초 ===")

# 튜플 생성
coordinates = (3, 5)  # 좌표
rgb_color = (255, 128, 0)  # RGB 색상
person_info = ("김파이썬", 25, "서울")  # 이름, 나이, 도시

print("좌표:", coordinates)
print("RGB 색상:", rgb_color)
print("개인정보:", person_info)

# 단일 요소 튜플 (쉼표 필수!)
single_tuple = (42,)  # 쉼표가 없으면 그냥 괄호로 인식
print("단일 튜플:", single_tuple)

# 괄호 없이도 가능
point = 10, 20
print("괄호 없는 튜플:", point)

print("\n=== 튜플 접근과 언패킹 ===")

# 인덱싱 (리스트와 동일)
person = ("홍길동", 30, "부산", "엔지니어")
print(f"이름: {person[0]}")
print(f"나이: {person[1]}")
print(f"마지막 정보: {person[-1]}")

# 슬라이싱
print(f"이름과 나이: {person[:2]}")

# 튜플 언패킹 (Unpacking)
name, age, city, job = person
print(f"언패킹 결과 - 이름: {name}, 나이: {age}, 도시: {city}, 직업: {job}")

# 일부만 언패킹 (*rest 사용)
first, second, *rest = (1, 2, 3, 4, 5)
print(f"첫 번째: {first}, 두 번째: {second}, 나머지: {rest}")

# 변수 교환 (튜플의 멋진 활용)
a, b = 10, 20
print(f"교환 전: a={a}, b={b}")
a, b = b, a  # 튜플 언패킹으로 교환
print(f"교환 후: a={a}, b={b}")

print("\n=== 튜플 실습 예제 ===")

# 학생 정보 관리 (튜플로 불변 데이터)
students_info = [
    ("김철수", 20, "컴퓨터공학", 85),
    ("이영희", 21, "경영학", 92),
    ("박민수", 19, "수학", 78),
    ("최영수", 22, "물리학", 95)
]

print("학생 정보 목록:")
for student in students_info:
    name, age, major, grade = student
    print(f"이름: {name}, 나이: {age}, 전공: {major}, 성적: {grade}")

# 전공별 평균 성적
majors = {}
for name, age, major, grade in students_info:
    if major not in majors:
        majors[major] = []
    majors[major].append(grade)

print("\n전공별 평균 성적:")
for major, grades in majors.items():
    average = sum(grades) / len(grades)
    print(f"{major}: {average:.1f}점")

# ===================================================================
# 3. 딕셔너리 (Dictionary) - 키-값 쌍의 데이터 집합
# ===================================================================

print("\n=== 딕셔너리 기초 ===")

# 딕셔너리 생성
student = {
    "name": "김파이썬",
    "age": 25,
    "major": "컴퓨터공학",
    "grades": [85, 92, 78, 95]
}

print("학생 딕셔너리:", student)

# 빈 딕셔너리
empty_dict = {}
print("빈 딕셔너리:", empty_dict)

print("\n=== 딕셔너리 접근과 수정 ===")

# 값 접근
print(f"이름: {student['name']}")
print(f"나이: {student['age']}")

# get() 메서드 (키가 없어도 에러 없음)
print(f"전화번호: {student.get('phone', '정보 없음')}")

# 값 수정
student["age"] = 26
print("나이 수정 후:", student["age"])

# 새 키-값 추가
student["phone"] = "010-1234-5678"
student["address"] = "서울시 강남구"
print("정보 추가 후:", student)

# 키 삭제
del student["address"]
print("주소 삭제 후:", student)

# pop() - 키 삭제하고 값 반환
phone = student.pop("phone")
print(f"삭제된 전화번호: {phone}")
print("전화번호 삭제 후:", student)

print("\n=== 딕셔너리 메서드 ===")

# keys(), values(), items()
student = {"name": "김파이썬", "age": 25, "major": "컴퓨터공학"}

print("모든 키:", list(student.keys()))
print("모든 값:", list(student.values()))
print("모든 키-값 쌍:", list(student.items()))

# 딕셔너리 순회
print("\n딕셔너리 순회:")
for key in student:
    print(f"{key}: {student[key]}")

print("\n키-값 쌍으로 순회:")
for key, value in student.items():
    print(f"{key}: {value}")

# update() - 다른 딕셔너리로 업데이트
additional_info = {"gpa": 3.8, "semester": 6}
student.update(additional_info)
print("정보 업데이트 후:", student)

print("\n=== 딕셔너리 실습 예제 ===")

# 단어 카운터
text = "python is great python is fun python programming"
words = text.split()

word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print("단어 개수:", word_count)

# 더 간단한 방법 (get 활용)
word_count2 = {}
for word in words:
    word_count2[word] = word_count2.get(word, 0) + 1

print("단어 개수 (get 사용):", word_count2)

# 학급 성적 관리 시스템
classroom = {
    "김철수": {"korean": 85, "english": 92, "math": 78},
    "이영희": {"korean": 92, "english": 88, "math": 95},
    "박민수": {"korean": 78, "english": 85, "math": 82}
}

print("\n학급 성적 관리:")
for name, subjects in classroom.items():
    total = sum(subjects.values())
    average = total / len(subjects)
    print(f"{name}: 총점 {total}, 평균 {average:.1f}")

# 과목별 평균
subject_totals = {"korean": 0, "english": 0, "math": 0}
student_count = len(classroom)

for name, subjects in classroom.items():
    for subject, score in subjects.items():
        subject_totals[subject] += score

print("\n과목별 평균:")
for subject, total in subject_totals.items():
    average = total / student_count
    print(f"{subject}: {average:.1f}점")

# ===================================================================
# 4. 집합 (Set) - 중복 없는 데이터 집합
# ===================================================================

print("\n=== 집합 기초 ===")

# 집합 생성
fruits = {"사과", "바나나", "오렌지"}
numbers = {1, 2, 3, 4, 5}
mixed_set = {"파이썬", 42, 3.14}

print("과일 집합:", fruits)
print("숫자 집합:", numbers)
print("혼합 집합:", mixed_set)

# 빈 집합 (주의: {}는 딕셔너리!)
empty_set = set()
print("빈 집합:", empty_set)

# 리스트에서 집합 생성 (중복 제거됨)
duplicate_numbers = [1, 2, 2, 3, 3, 3, 4, 5, 5]
unique_numbers = set(duplicate_numbers)
print("중복 있는 리스트:", duplicate_numbers)
print("중복 제거된 집합:", unique_numbers)

print("\n=== 집합 연산 ===")

# 요소 추가/제거
fruits = {"사과", "바나나"}
print("초기 집합:", fruits)

fruits.add("오렌지")
print("오렌지 추가:", fruits)

fruits.remove("바나나")  # 없으면 에러
print("바나나 제거:", fruits)

fruits.discard("포도")  # 없어도 에러 없음
print("포도 제거 시도:", fruits)

# 집합 연산
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

print(f"집합1: {set1}")
print(f"집합2: {set2}")

# 합집합 (Union)
union = set1 | set2
print(f"합집합: {union}")

# 교집합 (Intersection)
intersection = set1 & set2
print(f"교집합: {intersection}")

# 차집합 (Difference)
difference = set1 - set2
print(f"차집합 (set1 - set2): {difference}")

# 대칭차집합 (Symmetric Difference)
symmetric_diff = set1 ^ set2
print(f"대칭차집합: {symmetric_diff}")

print("\n=== 집합 실습 예제 ===")

# 학생 과목 수강 관리
math_students = {"김철수", "이영희", "박민수", "최영수"}
science_students = {"이영희", "박민수", "한지민", "정수진"}
english_students = {"김철수", "한지민", "정수진", "조민호"}

print("수학 수강생:", math_students)
print("과학 수강생:", science_students)
print("영어 수강생:", english_students)

# 두 과목 이상 수강하는 학생
multi_subject = (math_students & science_students) | \
                (math_students & english_students) | \
                (science_students & english_students)
print("두 과목 이상 수강:", multi_subject)

# 모든 과목 수강하는 학생
all_subjects = math_students & science_students & english_students
print("모든 과목 수강:", all_subjects)

# 전체 학생 수
all_students = math_students | science_students | english_students
print("전체 학생:", all_students)
print("전체 학생 수:", len(all_students))

# 한 과목만 수강하는 학생
only_math = math_students - science_students - english_students
only_science = science_students - math_students - english_students
only_english = english_students - math_students - science_students
single_subject = only_math | only_science | only_english

print("한 과목만 수강:", single_subject)

# ===================================================================
# 5. 데이터 구조 조합 활용
# ===================================================================

print("\n=== 데이터 구조 조합 활용 ===")

# 복잡한 데이터 구조 - 학교 관리 시스템
school_data = {
    "students": [
        {
            "id": 1,
            "name": "김철수",
            "age": 20,
            "grades": {"math": 85, "science": 92, "english": 78},
            "hobbies": {"독서", "영화감상", "게임"}
        },
        {
            "id": 2,
            "name": "이영희",
            "age": 21,
            "grades": {"math": 95, "science": 88, "english": 92},
            "hobbies": {"음악", "독서", "운동"}
        },
        {
            "id": 3,
            "name": "박민수",
            "age": 19,
            "grades": {"math": 78, "science": 85, "english": 82},
            "hobbies": {"게임", "영화감상", "요리"}
        }
    ],
    "teachers": {
        "math": "김수학",
        "science": "이과학",
        "english": "박영어"
    },
    "courses": ["math", "science", "english"]
}

# 데이터 분석
print("학교 데이터 분석:")
print(f"전체 학생 수: {len(school_data['students'])}명")
print(f"과목 수: {len(school_data['courses'])}개")

# 각 학생 정보 출력
for student in school_data["students"]:
    name = student["name"]
    age = student["age"]
    
    # 평균 성적 계산
    grades = student["grades"]
    average = sum(grades.values()) / len(grades)
    
    # 취미 개수
    hobby_count = len(student["hobbies"])
    
    print(f"\n{name} (ID: {student['id']}):")
    print(f"  나이: {age}세")
    print(f"  평균 성적: {average:.1f}점")
    print(f"  취미: {', '.join(student['hobbies'])} ({hobby_count}개)")

# 과목별 평균 성적
subject_averages = {}
for subject in school_data["courses"]:
    total = sum(student["grades"][subject] for student in school_data["students"])
    average = total / len(school_data["students"])
    subject_averages[subject] = average

print("\n과목별 평균 성적:")
for subject, average in subject_averages.items():
    teacher = school_data["teachers"][subject]
    print(f"{subject}: {average:.1f}점 (담당: {teacher} 선생님)")

# 공통 취미 찾기
all_hobbies = set()
for student in school_data["students"]:
    all_hobbies.update(student["hobbies"])

print(f"\n전체 취미 목록: {all_hobbies}")

# 가장 인기 있는 취미
hobby_count = {}
for student in school_data["students"]:
    for hobby in student["hobbies"]:
        hobby_count[hobby] = hobby_count.get(hobby, 0) + 1

print("\n취미별 인기도:")
for hobby, count in sorted(hobby_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{hobby}: {count}명")

# ===================================================================
# 6. 리스트 컴프리헨션 (List Comprehension)
# ===================================================================

print("\n=== 리스트 컴프리헨션 ===")

# 기본 리스트 컴프리헨션
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 일반적인 방법
squares = []
for num in numbers:
    squares.append(num ** 2)
print("일반 방법 - 제곱수:", squares)

# 리스트 컴프리헨션
squares_comp = [num ** 2 for num in numbers]
print("컴프리헨션 - 제곱수:", squares_comp)

# 조건 포함
even_squares = [num ** 2 for num in numbers if num % 2 == 0]
print("짝수의 제곱:", even_squares)

# 복잡한 표현식
words = ["python", "java", "javascript", "go"]
word_info = [f"{word.upper()}({len(word)}글자)" for word in words]
print("단어 정보:", word_info)

# 중첩 리스트 평탄화
nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for sublist in nested_list for item in sublist]
print("중첩 리스트:", nested_list)
print("평탄화된 리스트:", flattened)

# 딕셔너리 컴프리헨션
numbers = [1, 2, 3, 4, 5]
square_dict = {num: num ** 2 for num in numbers}
print("딕셔너리 컴프리헨션:", square_dict)

# 집합 컴프리헨션
text = "hello world"
unique_chars = {char.upper() for char in text if char.isalpha()}
print("고유 문자 집합:", unique_chars)

print("\n=== 7단계 완료! ===")
print("데이터 구조를 모두 배웠습니다.")
print("다음 단계에서는 문자열 심화를 배워보겠습니다!")

# ===================================================================
# 추가 팁
# ===================================================================

"""
7단계에서 기억해야 할 중요한 점들:

1. 리스트 (List): 순서 있음, 변경 가능, 중복 허용
   - 인덱싱, 슬라이싱, append(), insert(), remove(), pop() 등

2. 튜플 (Tuple): 순서 있음, 변경 불가능, 중복 허용
   - 좌표, 설정값 등 변하지 않는 데이터에 사용
   - 언패킹으로 여러 변수에 동시 할당

3. 딕셔너리 (Dictionary): 키-값 쌍, 순서 있음(3.7+), 중복 키 불가
   - get(), keys(), values(), items(), update() 등
   - 빠른 검색과 매핑에 사용

4. 집합 (Set): 순서 없음, 중복 불가, 변경 가능
   - 교집합, 합집합, 차집합 등 수학적 연산
   - 중복 제거와 멤버십 테스트에 유용

5. 적절한 자료구조 선택이 중요:
   - 순서가 중요하면 리스트/튜플
   - 키로 검색하면 딕셔너리
   - 중복 제거나 집합 연산이면 셋

실습할 때 꼭 해보세요:
- 각 자료구조의 메서드들 활용하기
- 복잡한 데이터를 조합해서 관리하기
- 리스트 컴프리헨션으로 간결한 코드 작성하기
- 실제 문제에 적합한 자료구조 선택하기
"""
