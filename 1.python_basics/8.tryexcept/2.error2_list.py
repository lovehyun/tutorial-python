# 1. 리스트 활용시 발생할 수 있는 에러
numbers = [1, 2, 3, 4, 5]

try:
    index = 10
    value = numbers[index]
    print("인덱스", index, "의 값:", value)
except IndexError:
    print("유효하지 않은 인덱스입니다.")
