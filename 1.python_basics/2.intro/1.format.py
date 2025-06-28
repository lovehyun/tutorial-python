# 1. 일반 문자열 출력:
name = "Alice"
print("Hello, " + name + "!")

# 2. f-문자열 (f-string) 사용:
name = "Alice"
print(f"Hello, {name}!")

# 3. 문자열 포맷팅 사용:
name = "Alice"
print("Hello, {}!".format(name))

# 4. format() 메서드와 인덱스 사용:
name = "Alice"
print("Hello, {0}!".format(name))

# 5. 문자열 연결 연산자 사용:
name = "Alice"
print("Hello, ", end="")
print(name, end="")
print("!")

# 6. % 연산자 사용:
name = "Alice"
print("Hello, %s!" % name)

# 7. join() 메서드 사용:
name = "Alice"
print("Hello, " + "".join(name) + "!")
