# 1. 튜플(Tuple) 활용
# 여러 값을 동시에 반환하기
def get_name_and_age():
    name = "John"
    age = 25
    return name, age

name, age = get_name_and_age()
print("Name:", name)
print("Age:", age)
# 출력: Name: John, Age: 25

# 2. 리스트(List) 활용
# 동적인 크기와 순서가 있는 데이터 저장
shopping_list = ["apple", "banana", "orange"]
shopping_list.append("grape")
shopping_list.remove("banana")
print(shopping_list)
# 출력: ["apple", "orange", "grape"]

# 3. 딕셔너리(Dictionary) 활용
# 키-값 쌍으로 데이터 관리
student = {
    "name": "John",
    "age": 20,
    "university": "ABC University"
}
print("Name:", student["name"])
print("Age:", student["age"])
print("University:", student["university"])
# 출력: Name: John, Age: 20, University: ABC University

