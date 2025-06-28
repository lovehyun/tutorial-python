# 가변 인자 처리

# 1. *args 사용
def sum_all(*args):
    return sum(args)

# 사용 예시
result = sum_all(1, 2, 3, 4, 5)
print(result)  # 출력: 15


# 2. **kwargs 사용
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

# 사용 예시
print_kwargs(name="Alice", age=30, city="New York")
# 출력:
# name = Alice
# age = 30
# city = New York


# 3. *args 와 **kwargs 를 함께 사용
def mixed_args(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

# 사용 예시
mixed_args(1, 2, 3, name="Alice", age=30)
# 출력:
# Positional arguments: (1, 2, 3)
# Keyword arguments: {'name': 'Alice', 'age': 30}


# 4. 기본 인자와 함께 사용
def greet(message, *args):
    print(message)
    for name in args:
        print(f"Hello, {name}!")

# 사용 예시
greet("Welcome everyone!", "Alice", "Bob", "Charlie")
# 출력:
# Welcome everyone!
# Hello, Alice!
# Hello, Bob!
# Hello, Charlie!
