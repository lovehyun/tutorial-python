# 1. items() 기본 예제
# 딕셔너리 생성
my_dict = {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'}

# items() 메서드 사용
items = my_dict.items()

# items() 결과 출력
print(items)  # dict_items([('name', 'Alice'), ('age', 25), ('phone', '123-456-7890')])

# items()를 리스트로 변환하여 출력
print(list(items))  # [('name', 'Alice'), ('age', 25), ('phone', '123-456-7890')]


# -----
# 2. 반복문에서 사용 예제
# 딕셔너리 생성
my_dict = {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'}

# items()를 사용하여 반복문으로 딕셔너리 항목 출력
for key, value in my_dict.items():
    print(f'Key: {key}, Value: {value}')
# Key: name, Value: Alice
# Key: age, Value: 25
# Key: phone, Value: 123-456-7890


# -----
# 3-1. 딕셔너리 항목을 정렬하여 출력

# 딕셔너리 생성
my_dict = {'name': 'Charlie', 'age': 35, 'phone': '555-123-4567', 'city': 'New York'}

# items()와 sorted()를 사용하여 키로 정렬하여 출력
for key, value in sorted(my_dict.items()):
    print(f'Key: {key}, Value: {value}')
# Key: age, Value: 35
# Key: city, Value: New York
# Key: name, Value: Charlie
# Key: phone, Value: 555-123-4567


# 3-2. 딕셔너리 업데이트

# 딕셔너리 생성
my_dict = {'name': 'Alice', 'age': 25}

# 다른 딕셔너리 생성
update_dict = {'phone': '123-456-7890', 'city': 'Wonderland'}

# items()를 사용하여 기존 딕셔너리 업데이트
for key, value in update_dict.items():
    my_dict[key] = value

print(my_dict)  # {'name': 'Alice', 'age': 25, 'phone': '123-456-7890', 'city': 'Wonderland'}


# 3-3. 딕셔너리 조건에 따른 필터링

# 딕셔너리 생성
my_dict = {'name': 'Alice', 'age': 25, 'phone': '123-456-7890', 'city': 'Wonderland'}

# items()를 사용하여 특정 조건을 만족하는 항목만 필터링
filtered_dict = {key: value for key, value in my_dict.items() if isinstance(value, str)}

print(filtered_dict)  # {'name': 'Alice', 'phone': '123-456-7890', 'city': 'Wonderland'}

