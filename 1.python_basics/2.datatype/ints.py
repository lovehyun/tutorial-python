# 1. 수학 연산
# int 클래스는 기본적인 수학 연산을 지원합니다.

x = 5
y = 3

# 덧셈
print(x + y)  # 8

# 뺄셈
print(x - y)  # 2

# 곱셈
print(x * y)  # 15

# 나눗셈
print(x / y)  # 1.6666666666666667

# 나머지
print(x % y)  # 2

# 거듭제곱
print(x ** y)  # 125


# 2. 진법 변환
x = 10

# 2진수로 변환
print(bin(x))  # '0b1010'

# 8진수로 변환
print(oct(x))  # '0o12'

# 16진수로 변환
print(hex(x))  # '0xa'


# 3. 기타 메서드
x = 123

# 절댓값 구하기
print(abs(x))  # 123

# 정수로 변환
y = 4.5
print(int(y))  # 4

# 문자열을 정수로 변환
str_num = "100"
print(int(str_num))  # 100


# 4. 비트 연산
x = 5
y = 3

# 비트 AND
print(x & y)  # 1

# 비트 OR
print(x | y)  # 7

# 비트 XOR
print(x ^ y)  # 6

# 비트 NOT
print(~x)  # -6

# 비트 왼쪽 시프트
print(x << 1)  # 10

# 비트 오른쪽 시프트
print(x >> 1)  # 2
