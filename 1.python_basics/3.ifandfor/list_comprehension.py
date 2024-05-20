# [표현식 for 항목 in iterable if 조건문]

# 1부터 10까지의 제곱 값들로 이루어진 리스트 생성
squares = [x ** 2 for x in range(1, 11)]
print(squares)
# 출력: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 1부터 20까지의 짝수들로 이루어진 리스트 생성
even_numbers = [x for x in range(1, 21) if x % 2 == 0]
print(even_numbers)
# 출력: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# 문자열의 각 글자를 대문자로 변환한 리스트 생성
word = "hello"
upper_letters = [char.upper() for char in word]
print(upper_letters)
# 출력: ['H', 'E', 'L', 'L', 'O']
