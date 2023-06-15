# 1. 리스트 순회하기
numbers = [1, 2, 3, 4, 5]

for num in numbers:
    if num % 2 == 0:
        print(num, "is even")
    else:
        print(num, "is odd")


# 2. 조건에 맞는 항목 필터링하기
even_numbers = []
for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
print("Even numbers:", even_numbers)


# 3. 딕셔너리의 키-값 쌍 순회하기
student_grades = {"John": 85, "Emily": 92, "Michael": 78, "Sophia": 95}
for name, grade in student_grades.items():
    if grade >= 90:
        print(name, "has an A grade")
    else:
        print(name, "does not have an A grade")

