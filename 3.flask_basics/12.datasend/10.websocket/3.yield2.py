def test():

    print("A")
    yield 1

    print("B")
    yield 2

    print("C")
    yield 3

x = test()

print(next(x))
print(next(x))
print(next(x))
# print(next(x))  # 여기에서 예외 발생

# A
# 1
# B
# 2
# C
# 3

# 예외 처리 코드 추가
# try:
#     while True:
#         print(next(x))
# except StopIteration:
#     print("모든 데이터 사용 완료")
