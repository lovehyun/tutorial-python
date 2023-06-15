def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n+1):
            result *= i
        return result

n = int(input("팩토리얼을 계산할 숫자를 입력하세요: "))
result = factorial(n)

print("팩토리얼:", result)
