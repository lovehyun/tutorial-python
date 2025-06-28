# 선형탐색 (Linear Search)
def linear_search(arr, target):
    for index in range(len(arr)):
        if arr[index] == target:
            return index
    return -1

# 이진탐색 (Binary Search)
# 정렬된 배열에서 특정 값을 찾는 효율적인 탐색 방법으로, 매번 탐색 범위를 절반씩 줄여나가면서 목표값을 찾습니다.
# 전제 조건: 배열이 정렬되어 있어야 함
# 시간 복잡도: O(log n) - 매우 효율적
# 공간 복잡도: O(1) - 추가 메모리 사용 최소
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
