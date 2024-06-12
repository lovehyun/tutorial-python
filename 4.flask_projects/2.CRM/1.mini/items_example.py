# 1. items() 기본 예제
# 딕셔너리 생성
my_dict = {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'}

keys = my_dict.keys()
values = my_dict.values()

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

# 참고 - Python 3.9 이상~ 
merged_dict = my_dict | update_dict
print(merged_dict)


# 3-3. 딕셔너리 조건에 따른 필터링

# 딕셔너리 생성
my_dict = {'name': 'Alice', 'age': 25, 'phone': '123-456-7890', 'city': 'Wonderland'}

# items()를 사용하여 특정 조건을 만족하는 항목만 필터링 - 값(value) 이 문자열(str) 인 항목만 출력
filtered_dict = {key: value for key, value in my_dict.items() if isinstance(value, str)}

print(filtered_dict)  # {'name': 'Alice', 'phone': '123-456-7890', 'city': 'Wonderland'}

# items()를 사용하여 특정 조건을 만족하는 항목만 필터링
filtered_dict = {key: value for key, value in my_dict.items() if key == 'age' and value >= 20}

print(filtered_dict)  # {'age': 25}


# 3-4. 딕셔너리 리스트 처리 예제

# 딕셔너리의 리스트 생성
my_dicts = [
    {'name': 'Alice', 'age': 25, 'phone': '123-456-7890', 'city': 'Wonderland'},
    {'name': 'Bob', 'age': 19, 'phone': '987-654-3210', 'city': 'Dreamland'},
    {'name': 'Charlie', 'age': 22, 'phone': '555-666-7777', 'city': 'Fantasia'}
]

# 나이가 20살 이상인 항목만 필터링
filtered_dicts = [{key: value for key, value in d.items() if key == 'age' and value >= 20} for d in my_dicts]

print(filtered_dicts)
# [{'age': 25}, {}, {'age': 22}]

# 나이가 20살 이상인 항목만 포함된 딕셔너리들로 구성된 리스트 생성
filtered_dicts = [d for d in my_dicts if d.get('age', 0) >= 20]

print(filtered_dicts)
# [{'name': 'Alice', 'age': 25, 'phone': '123-456-7890', 'city': 'Wonderland'}, {'name': 'Charlie', 'age': 22, 'phone': '555-666-7777', 'city': 'Fantasia'}]

# 참고: 나이가 20살 이상인 항목만 포함된 딕셔너리들로 구성된 리스트 생성
filtered_dicts = []
for d in my_dicts:
    # if d.get('age', 0) >= 20:
    if d['age'] >= 20:
        filtered_dicts.append(d)
