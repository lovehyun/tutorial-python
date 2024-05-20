# 이진탐색 (Binary Search)
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

# 이진 탐색 사용 예제
arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
target = 7
result = binary_search(arr, target)
if result != -1:
    print("타겟의 인덱스:", result)
else:
    print("타겟이 존재하지 않습니다.")
