# 1. 인자 1개
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")


# 2. 인자 2개
def add(x, y):
    return x + y

result = add(3, 5)
print(result)


# 3. 인자 3개
def power(base, exponent, message):
    result = base ** exponent
    print(f"{base}의 {exponent} 제곱은 {result}. {message}")

power(2, 3, "계산 완료")


# 4. 가변 인자
def concatenate(*args):
    result = ""
    for word in args:
        result += word
    return result

print(concatenate("Hello", " ", "World", "!"))


# 5. 키워드 인자
def greet_with_message(name, message):
    print(f"{message}, {name}!")

greet_with_message(message="안녕하세요", name="Bob")


# 6. 기본값 인자
def greet_default(name="Guest"):
    print(f"Hello, {name}!")

greet_default()
greet_default("Alice")


# 7. 위치 인자와 키워드 인자 혼합
def example(a, b, c):
    print(f"a: {a}, b: {b}, c: {c}")

example(1, 2, 3)  # 위치 인자 사용
example(a=1, b=2, c=3)  # 키워드 인자 사용
example(1, c=3, b=2)  # 혼합하여 사용
