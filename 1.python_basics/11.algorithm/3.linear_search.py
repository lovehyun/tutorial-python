# 선형 탐색 (Linear Search)
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# 선형 탐색 사용 예제
arr = [5, 8, 3, 12, 7, 10]
target = 7
result = linear_search(arr, target)
if result != -1:
    print("타겟의 인덱스:", result)
else:
    print("타겟이 존재하지 않습니다.")


# 랜덤 숫자 리스트 생성하기
import random
def generate_random_numbers(count):
    random_numbers = [random.randint(1, 1000000) for _ in range(count)]
    return random_numbers
