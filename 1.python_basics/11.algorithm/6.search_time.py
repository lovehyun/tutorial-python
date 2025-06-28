import random
import time

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# 예제 데이터 생성
data_size = 10_000_000  # 데이터셋 크기
target = random.randint(0, data_size)  # 랜덤한 타겟 값 선택
data = random.sample(range(data_size), data_size)  # 0부터 data_size까지의 범위에서 중복되지 않는 랜덤한 값들로 리스트 생성

# Linear Search 수행 시간 측정
start_time = time.time()
linear_search(data, target)
end_time = time.time()
linear_search_time = end_time - start_time

# Binary Search 수행 시간 측정 (이전에 정렬이 필요)
sorted_data = sorted(data)  # 리스트를 정렬
start_time = time.time()
binary_search(sorted_data, target)
end_time = time.time()
binary_search_time = end_time - start_time

# 결과 출력
print("Linear Search 수행 시간:", linear_search_time)
print("Binary Search 수행 시간:", binary_search_time)
