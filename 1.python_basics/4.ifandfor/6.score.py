students = {
    '김철수': 70,
    '이영희': 82,
    '박민수': 88,
    '최지은': 75,
    '장현우': 93,
    '서민정': 67,
    '정우성': 99,
    '한지민': 76,
    '오세훈': 61,
    '송지효': 85
}

def get_a_students(students):
    a_students = []
    for name, score in students.items():
        if score >= 90:  # A 등급 조건
            a_students.append(name)
    return a_students

# 함수 실행
a_grade_students = get_a_students(students)
print("A 등급 학생:", a_grade_students)

###################################

# 등급을 반환하는 함수
def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    else:
        return 'F'

# A 이상 학생 찾기
def get_a_students(students):
    a_students = []
    for name, score in students.items():
        if get_grade(score) == 'A':
            a_students.append(name)
    return a_students

# 실행
a_grade_students = get_a_students(students)
print("A 등급 이상 학생:", a_grade_students)
