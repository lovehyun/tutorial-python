# 1. 리스트 요소의 제곱 계산하기
numbers = [1, 2, 3, 4, 5]
squared_numbers = [x**2 for x in numbers]
print(squared_numbers)
# 출력: [1, 4, 9, 16, 25]


# 2. 문자열의 글자 수 세기
words = ["apple", "banana", "cherry", "dragonfruit"]
word_lengths = [len(word) for word in words]
print(word_lengths)
# 출력: [5, 6, 6, 11]


# 3. 조건에 따라 필터링하기
numbers = [1, 2, 3, 4, 5]
even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)
# 출력: [2, 4]


# 4. 문자열 리스트에서 길이가 3 이하인 단어들만 선택하기
words = ["apple", "banana", "cherry", "dragonfruit", "egg"]
short_words = [word for word in words if len(word) <= 3]
print(short_words)
# 출력: ["egg"]


# 5. 중첩 리스트 펼치기
nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened_list = [num for sublist in nested_list for num in sublist]
print(flattened_list)
# 출력: [1, 2, 3, 4, 5, 6, 7, 8, 9]


# 6. 특정 조건을 만족하는 요소 필터링
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
greater_than_five = [x for x in numbers if x > 5]
print(greater_than_five)
# 출력: [6, 7, 8, 9, 10]


# 7. 문자열 리스트에서 첫 글자가 모음인 단어들 선택하기
words = ["apple", "banana", "cherry", "apricot", "egg"]
vowel_starting_words = [word for word in words if word[0].lower() in 'aeiou']
print(vowel_starting_words)
# 출력: ["apple", "apricot", "egg"]


# 8. 튜플 리스트를 딕셔너리로 변환하기
tuple_list = [("key1", "value1"), ("key2", "value2"), ("key3", "value3")]
dictionary = {key: value for key, value in tuple_list}
print(dictionary)
# 출력: {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}


# Advanced

# 10. 문자열 리스트에서 단어의 길이에 따라 단어를 역순으로 정렬한 후, 모든 단어를 대문자로 변환하기
words = ["apple", "banana", "cherry", "dragonfruit", "egg"]
sorted_uppercase_words = [word.upper() for word in sorted(words, key=len, reverse=True)]
print(sorted_uppercase_words)
# 출력: ['DRAGONFRUIT', 'BANANA', 'CHERRY', 'APPLE', 'EGG']


# 11. 중첩된 딕셔너리에서 특정 키의 값을 추출하여 리스트 생성하기
nested_dict = {
    "person1": {"name": "Alice", "age": 25},
    "person2": {"name": "Bob", "age": 30},
    "person3": {"name": "Charlie", "age": 35}
}
names = [info["name"] for person, info in nested_dict.items()]
print(names)
# 출력: ['Alice', 'Bob', 'Charlie']
