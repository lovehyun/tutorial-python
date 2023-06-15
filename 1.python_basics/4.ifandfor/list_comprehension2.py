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

