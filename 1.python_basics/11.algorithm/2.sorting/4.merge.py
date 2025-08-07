# 핵심 아이디어: "나누어서 정복하고 합치기"
# 시간복잡도: 항상 O(n log n) - 안정적!
# 공간복잡도: O(n) - 추가 메모리 필요
# 특징:
# - 안정 정렬 (같은 값의 순서 유지)
# - 최악의 경우에도 성능 보장
# - 큰 데이터 처리에 적합

def merge_sort(arr):
    """
    병합 정렬 알고리즘 (분할 정복)
    배열을 반으로 나누어 각각 정렬한 후 병합하는 방식
    """
    # 기저 조건: 원소가 1개 이하면 이미 정렬됨
    if len(arr) <= 1:
        return arr
    
    # 배열을 반으로 나누기
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # 재귀적으로 각 부분을 정렬
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    
    # 정렬된 두 부분을 병합
    return merge(left_sorted, right_sorted)

def merge(left, right):
    """
    두 개의 정렬된 배열을 하나의 정렬된 배열로 병합
    """
    result = []
    i = j = 0
    
    # 두 배열을 비교하면서 작은 값부터 result에 추가
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # 남은 원소들 추가
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def merge_sort_with_steps(arr, depth=0):
    """
    병합 정렬 과정을 단계별로 보여주는 버전
    """
    indent = "  " * depth
    print(f"{indent}분할: {arr}")
    
    if len(arr) <= 1:
        print(f"{indent}기저 조건: {arr}")
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    print(f"{indent}왼쪽: {left}, 오른쪽: {right}")
    
    # 재귀적으로 정렬
    left_sorted = merge_sort_with_steps(left, depth + 1)
    right_sorted = merge_sort_with_steps(right, depth + 1)
    
    # 병합
    result = merge_with_steps(left_sorted, right_sorted, depth)
    print(f"{indent}병합 완료: {result}")
    
    return result

def merge_with_steps(left, right, depth=0):
    """
    병합 과정을 단계별로 보여주는 함수
    """
    indent = "  " * depth
    print(f"{indent}병합 중: {left} + {right}")
    
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def merge_sort_iterative(arr):
    """
    반복적(비재귀) 병합 정렬
    """
    if len(arr) <= 1:
        return arr
    
    # 복사본 생성
    arr = arr.copy()
    n = len(arr)
    
    # 크기를 1부터 시작해서 2배씩 증가
    size = 1
    while size < n:
        # 현재 크기로 부분 배열들을 병합
        for start in range(0, n, size * 2):
            mid = min(start + size, n)
            end = min(start + size * 2, n)
            
            if mid < end:
                # 부분 배열 [start:mid]와 [mid:end]를 병합
                left = arr[start:mid]
                right = arr[mid:end]
                merged = merge(left, right)
                arr[start:end] = merged
        
        size *= 2
    
    return arr

def merge_sort_in_place(arr, left=0, right=None):
    """
    메모리 효율적인 병합 정렬 (제자리 정렬에 가까움)
    """
    if right is None:
        right = len(arr) - 1
    
    if left < right:
        mid = (left + right) // 2
        
        # 재귀적으로 정렬
        merge_sort_in_place(arr, left, mid)
        merge_sort_in_place(arr, mid + 1, right)
        
        # 병합
        merge_in_place(arr, left, mid, right)
    
    return arr

def merge_in_place(arr, left, mid, right):
    """
    제자리에서 병합 (추가 메모리 사용)
    """
    # 왼쪽과 오른쪽 부분 배열 복사
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    # 병합
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    # 남은 원소들 복사
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

# 테스트 코드
if __name__ == "__main__":
    # 테스트 데이터
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print("=== 병합 정렬 테스트 ===")
    print("원본 배열:", test_data)
    
    # 기본 병합 정렬
    result1 = merge_sort(test_data.copy())
    print("병합 정렬 결과:", result1)
    
    print("\n=== 단계별 병합 정렬 ===")
    result2 = merge_sort_with_steps(test_data.copy())
    
    print("\n=== 반복적 병합 정렬 ===")
    result3 = merge_sort_iterative(test_data.copy())
    print("반복적 병합 정렬 결과:", result3)
    
    print("\n=== 제자리 병합 정렬 ===")
    test_copy = test_data.copy()
    merge_sort_in_place(test_copy)
    print("제자리 병합 정렬 결과:", test_copy)
    
    # 성능 테스트
    import time
    import random
    
    print("\n=== 성능 테스트 ===")
    large_data = [random.randint(1, 1000) for _ in range(1000)]
    
    start_time = time.time()
    merge_sort(large_data.copy())
    end_time = time.time()
    print(f"1000개 원소 정렬 시간: {end_time - start_time:.4f}초")
    
    # 다른 테스트 케이스
    print("\n=== 다른 테스트 케이스 ===")
    test_cases = [
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # 이미 정렬됨
        [5, 4, 3, 2, 1],  # 역순
        [3, 3, 3, 3, 3],  # 모든 값이 같음
        [42],             # 원소 1개
        [],               # 빈 배열
    ]
    
    for i, data in enumerate(test_cases):
        original = data.copy()
        result = merge_sort(data.copy())
        print(f"테스트 {i + 1}: {original} -> {result}")
