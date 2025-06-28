# 1. lower()
# 문자열의 모든 문자를 소문자로 변환합니다.
s = "Hello World!"
print(s.lower())  # "hello world!"

# 2. upper()
# 문자열의 모든 문자를 대문자로 변환합니다.
s = "Hello World!"
print(s.upper())  # "HELLO WORLD!"

# 3. capitalize()
# 문자열의 첫 문자를 대문자로 변환하고 나머지 문자는 소문자로 변환합니다.
s = "hello world!"
print(s.capitalize())  # "Hello world!"

# 4. title()
# 문자열의 각 단어의 첫 문자를 대문자로 변환합니다.
s = "hello world!"
print(s.title())  # "Hello World!"

# 5. strip()
# 문자열 양쪽 끝의 공백(또는 다른 지정된 문자)을 제거합니다.
s = "  hello world!  "
print(s.strip())  # "hello world!"

# 6. lstrip()
# 문자열 왼쪽 끝의 공백(또는 다른 지정된 문자)을 제거합니다.
s = "  hello world!  "
print(s.lstrip())  # "hello world!  "

# 7. rstrip()
# 문자열 오른쪽 끝의 공백(또는 다른 지정된 문자)을 제거합니다.
s = "  hello world!  "
print(s.rstrip())  # "  hello world!"

# 8. replace()
# 문자열 내의 특정 부분 문자열을 다른 문자열로 대체합니다.
s = "hello world!"
print(s.replace("world", "Python"))  # "hello Python!"

# 9. split()
# 문자열을 특정 구분자를 기준으로 분할하여 리스트로 반환합니다.
s = "hello world!"
print(s.split())  # ['hello', 'world!']

s = "apple,banana,cherry"
print(s.split(","))  # ['apple', 'banana', 'cherry']

# 10. join()
# 리스트의 문자열 요소들을 특정 구분자로 결합하여 하나의 문자열로 만듭니다.
lst = ['hello', 'world']
print(" ".join(lst))  # "hello world"

lst = ['apple', 'banana', 'cherry']
print(",".join(lst))  # "apple,banana,cherry"

# 11. find()
# 문자열 내에서 특정 부분 문자열을 찾아 그 위치를 반환합니다. 찾지 못하면 -1을 반환합니다.
s = "hello world!"
print(s.find("world"))  # 6
print(s.find("Python"))  # -1

# 12. count()
# 문자열 내에서 특정 부분 문자열이 몇 번 나타나는지 셉니다.
s = "hello world! hello everyone!"
print(s.count("hello"))  # 2

# 13. startswith()
# 문자열이 특정 접두사로 시작하는지 확인합니다.
s = "hello world!"
print(s.startswith("hello"))  # True
print(s.startswith("world"))  # False

# 14. endswith()
# 문자열이 특정 접미사로 끝나는지 확인합니다.
s = "hello world!"
print(s.endswith("world!"))  # True
print(s.endswith("hello"))  # False
