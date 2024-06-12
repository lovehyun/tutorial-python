# 1. 두 리스트를 병렬로 묶기
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']

zipped = zip(list1, list2)
print(list(zipped))  # [(1, 'a'), (2, 'b'), (3, 'c')]


# 2. 세 개의 리스트를 병렬로 묶기
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [True, False, True]

zipped = zip(list1, list2, list3)
print(list(zipped))  # [(1, 'a', True), (2, 'b', False), (3, 'c', True)]


# 3. 짧은 이터러블을 기준으로 동작
list1 = [1, 2, 3]
list2 = ['a', 'b']

zipped = zip(list1, list2)
print(list(zipped))  # [(1, 'a'), (2, 'b')]


# 4. 묶인 리스트 풀기
zipped = [(1, 'a'), (2, 'b'), (3, 'c')]
unzipped = zip(*zipped)
list1, list2 = list(unzipped)

print(list1)  # [1, 2, 3]
print(list2)  # ['a', 'b', 'c']


# 5. 딕셔너리 생성
keys = ['name', 'age', 'phone']
values = ['Alice', 25, '123-456-7890']

dictionary = dict(zip(keys, values))
print(dictionary)  # {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'}


# 6. 딕셔너리 생성 - 리스트로부터
values_list = [
    ['Alice', 25, '123-456-7890'],
    ['Bob', 30, '987-654-3210'],
    ['Charlie', 22, '555-666-7777']
]
dictionaries = [dict(zip(keys, values)) for values in values_list]
print(dictionary)


# 7. 실용 예제 - 병렬 루프 처리
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]

for name, age in zip(names, ages):
    print(f'{name} is {age} years old.')
