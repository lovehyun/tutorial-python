def numbers():
    for i in range(100000000):
        yield i


for num in numbers():
    print(num)
    if num >= 10:
        break


# 위의 for 구문의 내부 동작 구조 - 굳이 next 안써도 됨

# iterator = iter(numbers())
# while True:
#     try:
#         num = next(iterator)
#         print(num)
#     except StopIteration:
#         break
