# 이진탐색 (Binary Search)
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    count = 0  # 비교 횟수 카운터

    while left <= right:
        count += 1  # 비교 시 카운트 증가
        mid = (left + right) // 2
        if arr[mid] == target:
            print(f"이진 탐색 비교 횟수: {count}회")
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    print(f"이진 탐색 비교 횟수: {count}회")
    return -1

# 선형탐색 (Linear Search)
def linear_search(arr, target):
    count = 0  # 비교 횟수 카운터

    for index in range(len(arr)):
        count += 1  # 비교 시 카운트 증가
        if arr[index] == target:
            print(f"선형 탐색 비교 횟수: {count}회")
            return index

    print(f"선형 탐색 비교 횟수: {count}회")
    return -1

# 예제 배열
# arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
# target = 7

arr = list(range(1, 1000001))  # 1부터 100만까지
target = 777777

# 이진 탐색 실행
result = binary_search(arr, target)
if result != -1:
    print("이진 탐색 결과 - 타겟의 인덱스:", result)
else:
    print("이진 탐색 결과 - 타겟이 존재하지 않습니다.")

# 선형 탐색 실행
result = linear_search(arr, target)
if result != -1:
    print("선형 탐색 결과 - 타겟의 인덱스:", result)
else:
    print("선형 탐색 결과 - 타겟이 존재하지 않습니다.")
