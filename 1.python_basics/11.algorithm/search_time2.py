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
data_size = 20  # 데이터셋 크기
target = random.randint(0, data_size)  # 랜덤한 타겟 값 선택
data = random.sample(range(data_size), data_size)  # 0부터 data_size까지의 범위에서 중복되지 않는 랜덤한 값들로 리스트 생성

# Linear Search 시각화
print("Linear Search")
print("Target:", target)
print("Data:", data)
print()

for i in range(len(data)):
    print(" " * 7, end="")
    if i > 0:
        print("   " * i, end="")

    print(data[i], "<--")

    if data[i] == target:
        break

print()

# Binary Search 시각화 (이전에 정렬이 필요)
sorted_data = sorted(data)  # 리스트를 정렬

print("Binary Search")
print("Target:", target)
print("Sorted Data:", sorted_data)
print()

left = 0
right = len(sorted_data) - 1
while left <= right:
    print(" " * 14, end="")
    mid = (left + right) // 2
    print("   " * mid, end="")
    print(sorted_data[mid], "<--")

    if sorted_data[mid] == target:
        break
    elif sorted_data[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

print()
