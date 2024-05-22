def factorial(n):
    result = 1
    for i in range(n, 0, -1):
        result *= i
    return result

# def factorial(n):
#     result = 1
#     for i in range(1, n + 1):
#         result *= i
#     return result

n = int(input("팩토리얼을 계산할 숫자를 입력하세요: "))
result = factorial(n)

print("팩토리얼:", result)
