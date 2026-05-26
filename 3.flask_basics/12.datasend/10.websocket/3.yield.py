# return = 함수 완전 종료
# yield = 잠깐 멈춤

# def test():
#     return 1
#     return 2

# print(test())


def test():

    yield 1
    yield 2
    yield 3


x = test()

print(next(x))
print(next(x))
print(next(x))


# yield 까지만 실행
# → 멈춤
# → 다음 next 때 이어서 실행
