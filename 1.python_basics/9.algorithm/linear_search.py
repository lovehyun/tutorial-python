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
