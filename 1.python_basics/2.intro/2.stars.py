# 1.
print('- 1 -')
# 1부터 5까지 반복
for i in range(1, 6):
    # i개의 별 출력
    print('*' * i)

# 1부터 5까지 반복
# for i in range(5, 0, -1):
#     # i개의 별 출력
#     print('*' * i)

# 2.
print('- 2 -')
# 총 줄 수
n = 5
# 1부터 n까지 반복
for i in range(1, n + 1):
    # (n-i)개의 공백과 i개의 별 출력
    print(' ' * (n - i) + '*' * i)


# 3.
print('- 3 -')
# 총 줄 수
n = 5
# 1부터 n까지 반복
for i in range(1, n + 1):
    # (n-i)개의 공백과 (2*i-1)개의 별 출력
    print(' ' * (n - i) + '*' * (2 * i - 1))


# 4.
print('- 4 -')
# 총 줄 수
n = 5

# 위쪽 마름모 출력
for i in range(1, n + 1):
    # (n-i)개의 공백과 (2*i-1)개의 별 출력
    print(' ' * (n - i) + '*' * (2 * i - 1))

# 아래쪽 마름모 출력
for i in range(n - 1, 0, -1):
    # (n-i)개의 공백과 (2*i-1)개의 별 출력
    print(' ' * (n - i) + '*' * (2 * i - 1))
