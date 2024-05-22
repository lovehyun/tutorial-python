# 1. 딕셔너리 생성 및 기본 연산
# 딕셔너리 생성
my_dict = {"name": "Alice", "age": 25, "location": "Seoul"}

# 딕셔너리 출력
print(my_dict)  # {'name': 'Alice', 'age': 25, 'location': 'Seoul'}

# 값 접근
print(my_dict["name"])  # Alice

# 값 변경
my_dict["age"] = 26
print(my_dict)  # {'name': 'Alice', 'age': 26, 'location': 'Seoul'}

# 새로운 키-값 쌍 추가
my_dict["car"] = "BMW"
print(my_dict)  # {'name': 'Alice', 'age': 26, 'location': 'Seoul', 'car': 'BMW'}


# 2. 딕셔너리 요소 삭제
# 특정 키-값 쌍 삭제
del my_dict["car"]
print(my_dict)  # {'name': 'Alice', 'age': 26, 'location': 'Seoul'}

# pop 메서드 사용
age = my_dict.pop("age")
print(age)  # 26
print(my_dict)  # {'name': 'Alice', 'location': 'Seoul'}

# popitem 메서드 사용 (마지막 요소 제거)
item = my_dict.popitem()
print(item)  # ('location', 'Seoul')
print(my_dict)  # {'name': 'Alice'}

# 모든 요소 삭제
my_dict.clear()
print(my_dict)  # {}


# 3. 딕셔너리 키와 값 접근
my_dict = {"name": "Alice", "age": 25, "location": "Seoul"}

# 키 접근
keys = my_dict.keys()
print(keys)  # dict_keys(['name', 'age', 'location'])

# 값 접근
values = my_dict.values()
print(values)  # dict_values(['Alice', 25, 'Seoul'])

# 키-값 쌍 접근
items = my_dict.items()
print(items)  # dict_items([('name', 'Alice'), ('age', 25), ('location', 'Seoul')])


# 4. 딕셔너리 메서드 활용
# get 메서드 사용 (키가 없을 때 기본값 반환)
name = my_dict.get("name")
print(name)  # Alice
car = my_dict.get("car", "No car")
print(car)  # No car

# setdefault 메서드 사용 (키가 없을 때 기본값 설정)
location = my_dict.setdefault("location", "Unknown")
print(location)  # Seoul
my_dict.setdefault("car", "BMW")
print(my_dict)  # {'name': 'Alice', 'age': 25, 'location': 'Seoul', 'car': 'BMW'}

# update 메서드 사용 (여러 요소 추가/업데이트)
my_dict.update({"age": 26, "job": "Engineer"})
print(my_dict)  # {'name': 'Alice', 'age': 26, 'location': 'Seoul', 'car': 'BMW', 'job': 'Engineer'}


# 5. 딕셔너리 내포 (Dict Comprehension)
# 딕셔너리 내포 사용
squares = {x: x**2 for x in range(6)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}


# 6. 딕셔너리의 복사
# 얕은 복사
my_dict = {"name": "Alice", "age": 25, "location": "Seoul"}
shallow_copy = my_dict.copy()
print(shallow_copy)  # {'name': 'Alice', 'age': 25, 'location': 'Seoul'}

# 깊은 복사 (내부 객체도 복사)
import copy
deep_copy = copy.deepcopy(my_dict)
print(deep_copy)  # {'name': 'Alice', 'age': 25, 'location': 'Seoul'}


# 7. 기타 유용한 메서드
# fromkeys 메서드 사용 (키의 리스트로 딕셔너리 생성)
keys = ["a", "b", "c"]
default_value = 0
new_dict = dict.fromkeys(keys, default_value)
print(new_dict)  # {'a': 0, 'b': 0, 'c': 0}

# dictionary를 리스트로 변환
key_list = list(my_dict.keys())
value_list = list(my_dict.values())
print(key_list)  # ['name', 'age', 'location']
print(value_list)  # ['Alice', 25, 'Seoul']

# 모든 키-값 쌍 출력
for key, value in my_dict.items():
    print(f"{key}: {value}")
# 출력:
# name: Alice
# age: 25
# location: Seoul


# 8. dict.fromkeys 사용
# fromkeys 메서드는 주어진 키들로 새로운 딕셔너리를 생성하고 모든 키에 대해 동일한 값을 할당합니다.

keys = ['a', 'b', 'c']
value = 0
new_dict = dict.fromkeys(keys, value)
print(new_dict)  # {'a': 0, 'b': 0, 'c': 0}


# 9. 딕셔너리 뷰 객체
# 딕셔너리의 키, 값, 키-값 쌍을 보기 위한 뷰 객체를 반환합니다.

my_dict = {'a': 1, 'b': 2, 'c': 3}

# 키 보기
keys_view = my_dict.keys()
print(keys_view)  # dict_keys(['a', 'b', 'c'])

# 값 보기
values_view = my_dict.values()
print(values_view)  # dict_values([1, 2, 3])

# 키-값 쌍 보기
items_view = my_dict.items()
print(items_view)  # dict_items([('a', 1), ('b', 2), ('c', 3)])


# 10. get 메서드로 기본값 제공
# get 메서드는 키가 존재하지 않을 때 기본값을 반환합니다.

value = my_dict.get('d', 'default_value')
print(value)  # default_value


# 11. setdefault 메서드
# setdefault 메서드는 키가 딕셔너리에 존재하지 않을 때만 값을 설정합니다.

my_dict = {'a': 1, 'b': 2}
value = my_dict.setdefault('c', 3)
print(my_dict)  # {'a': 1, 'b': 2, 'c': 3}


# 12. 딕셔너리 병합 (Python 3.9+)
# Python 3.9부터 두 딕셔너리를 병합할 수 있는 새로운 방법이 추가되었습니다.

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

# 병합 연산자 사용
merged_dict = dict1 | dict2
print(merged_dict)  # {'a': 1, 'b': 3, 'c': 4}

# 병합 후 업데이트
dict1 |= dict2
print(dict1)  # {'a': 1, 'b': 3, 'c': 4}


# 13. 딕셔너리 필터링
# 딕셔너리를 조건에 따라 필터링할 수 있습니다.

my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
filtered_dict = {k: v for k, v in my_dict.items() if v % 2 == 0}
print(filtered_dict)  # {'b': 2, 'd': 4}


# 14. zip 함수
# zip 함수는 여러 개의 iterable 객체(리스트, 튜플 등)를 병렬로 묶어주는 함수입니다. 보통은 이를 사용하여 키 리스트와 값 리스트를 딕셔너리로 변환할 때 유용하게 사용됩니다.

keys = ['a', 'b', 'c']
values = [1, 2, 3]

# zip 함수를 사용하여 딕셔너리 생성
my_dict = dict(zip(keys, values))
print(my_dict)  # {'a': 1, 'b': 2, 'c': 3}


# 15. 딕셔너리 역전
# 딕셔너리의 키와 값을 서로 뒤집는 방법입니다.

my_dict = {'a': 1, 'b': 2, 'c': 3}

# 딕셔너리 키와 값을 서로 뒤집음
flipped_dict = {v: k for k, v in my_dict.items()}
print(flipped_dict)  # {1: 'a', 2: 'b', 3: 'c'}


# 16. 딕셔너리 정렬
# 딕셔너리를 특정 기준으로 정렬할 수 있습니다.

my_dict = {'a': 3, 'b': 1, 'c': 2}

# 키를 기준으로 정렬
sorted_dict_by_key = dict(sorted(my_dict.items()))
print(sorted_dict_by_key)  # {'a': 3, 'b': 1, 'c': 2}

# 값을 기준으로 정렬
sorted_dict_by_value = dict(sorted(my_dict.items(), key=lambda x: x[1]))
print(sorted_dict_by_value)  # {'b': 1, 'c': 2, 'a': 3}


# 17. 딕셔너리 비교
# 두 개의 딕셔너리를 비교하여 동일한지 확인할 수 있습니다.

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 2, 'a': 1}

# 딕셔너리 비교
is_equal = dict1 == dict2
print(is_equal)  # True
