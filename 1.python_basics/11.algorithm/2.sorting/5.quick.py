# 핵심 아이디어: "피벗으로 나누고 각각 정렬"
# 시간복잡도: 평균 O(n log n), 최악 O(n²)
# 공간복잡도: 평균 O(log n) - 메모리 효율적
# 특징:
# - 평균적으로 가장 빠름
# - 제자리 정렬 가능
# - 피벗 선택이 성능에 큰 영향

def quick_sort(arr):
    """
    퀵 정렬 알고리즘 (분할 정복)
    피벗을 기준으로 작은 값과 큰 값을 나누어 정렬하는 방식
    """
    if len(arr) <= 1:
        return arr
    
    # 피벗 선택 (여기서는 중간 원소)
    pivot = arr[len(arr) // 2]
    
    # 피벗을 기준으로 분할
    left = [x for x in arr if x < pivot]      # 피벗보다 작은 값들
    middle = [x for x in arr if x == pivot]   # 피벗과 같은 값들
    right = [x for x in arr if x > pivot]     # 피벗보다 큰 값들
    
    # 재귀적으로 정렬 후 합치기
    return quick_sort(left) + middle + quick_sort(right)

def quick_sort_in_place(arr, low=0, high=None):
    """
    제자리 퀵 정렬 (메모리 효율적)
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # 파티션 수행
        pivot_index = partition(arr, low, high)
        
        # 피벗 기준으로 왼쪽과 오른쪽 재귀 정렬
        quick_sort_in_place(arr, low, pivot_index - 1)
        quick_sort_in_place(arr, pivot_index + 1, high)
    
    return arr

def partition(arr, low, high):
    """
    호어(Hoare) 파티션 방식
    마지막 원소를 피벗으로 선택하여 분할
    """
    # 마지막 원소를 피벗으로 선택
    pivot = arr[high]
    
    # 작은 원소들의 인덱스
    i = low - 1
    
    for j in range(low, high):
        # 현재 원소가 피벗보다 작거나 같으면
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # 피벗을 올바른 위치에 배치
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_with_steps(arr, depth=0):
    """
    퀵 정렬 과정을 단계별로 보여주는 버전
    """
    indent = "  " * depth
    print(f"{indent}정렬할 배열: {arr}")
    
    if len(arr) <= 1:
        print(f"{indent}기저 조건: {arr}")
        return arr
    
    # 피벗 선택
    pivot = arr[len(arr) // 2]
    print(f"{indent}피벗: {pivot}")
    
    # 분할
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    print(f"{indent}분할 결과:")
    print(f"{indent}  작은 값들: {left}")
    print(f"{indent}  피벗값들: {middle}")
    print(f"{indent}  큰 값들: {right}")
    
    # 재귀 정렬
    left_sorted = quick_sort_with_steps(left, depth + 1)
    right_sorted = quick_sort_with_steps(right, depth + 1)
    
    result = left_sorted + middle + right_sorted
    print(f"{indent}합병 결과: {result}")
    
    return result

def quick_sort_random_pivot(arr):
    """
    랜덤 피벗을 사용하는 퀵 정렬 (최악의 경우 방지)
    """
    import random
    
    if len(arr) <= 1:
        return arr
    
    # 랜덤 피벗 선택
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort_random_pivot(left) + middle + quick_sort_random_pivot(right)

def quick_sort_three_way(arr):
    """
    3-way 퀵 정렬 (중복값이 많을 때 효율적)
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[0]
    
    # 3개 그룹으로 분할
    less = []
    equal = []
    greater = []
    
    for x in arr:
        if x < pivot:
            less.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            greater.append(x)
    
    return quick_sort_three_way(less) + equal + quick_sort_three_way(greater)

def median_of_three_pivot(arr, low, high):
    """
    3개 값의 중간값을 피벗으로 선택 (더 좋은 피벗 선택)
    """
    mid = (low + high) // 2
    
    # 3개 값을 정렬
    if arr[mid] < arr[low]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[high] < arr[low]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[high] < arr[mid]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    # 중간값을 맨 끝으로 이동
    arr[mid], arr[high] = arr[high], arr[mid]
    return arr[high]

def quick_sort_optimized(arr, low=0, high=None):
    """
    최적화된 퀵 정렬
    - 3개 값의 중간값을 피벗으로 사용
    - 작은 배열에서는 삽입 정렬 사용
    """
    if high is None:
        high = len(arr) - 1
    
    # 작은 배열에서는 삽입 정렬이 더 빠름
    if high - low + 1 <= 10:
        insertion_sort_range(arr, low, high)
        return arr
    
    if low < high:
        # 중간값 피벗 사용
        median_of_three_pivot(arr, low, high)
        pivot_index = partition(arr, low, high)
        
        quick_sort_optimized(arr, low, pivot_index - 1)
        quick_sort_optimized(arr, pivot_index + 1, high)
    
    return arr

def insertion_sort_range(arr, low, high):
    """
    특정 범위에서만 삽입 정렬 수행
    """
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# 테스트 코드
if __name__ == "__main__":
    # 테스트 데이터
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print("=== 퀵 정렬 테스트 ===")
    print("원본 배열:", test_data)
    
    # 기본 퀵 정렬
    result1 = quick_sort(test_data.copy())
    print("퀵 정렬 결과:", result1)
    
    print("\n=== 단계별 퀵 정렬 ===")
    result2 = quick_sort_with_steps(test_data.copy())
    
    print("\n=== 제자리 퀵 정렬 ===")
    test_copy = test_data.copy()
    quick_sort_in_place(test_copy)
    print("제자리 퀵 정렬 결과:", test_copy)
    
    print("\n=== 랜덤 피벗 퀵 정렬 ===")
    result3 = quick_sort_random_pivot(test_data.copy())
    print("랜덤 피벗 퀵 정렬 결과:", result3)
    
    print("\n=== 3-way 퀵 정렬 ===")
    duplicate_data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print("중복값이 있는 배열:", duplicate_data)
    result4 = quick_sort_three_way(duplicate_data.copy())
    print("3-way 퀵 정렬 결과:", result4)
    
    print("\n=== 최적화된 퀵 정렬 ===")
    test_copy2 = test_data.copy()
    quick_sort_optimized(test_copy2)
    print("최적화된 퀵 정렬 결과:", test_copy2)
    
    # 성능 테스트
    import time
    import random
    
    print("\n=== 성능 테스트 ===")
    large_data = [random.randint(1, 1000) for _ in range(1000)]
    
    # 기본 퀵 정렬
    start_time = time.time()
    quick_sort(large_data.copy())
    end_time = time.time()
    print(f"기본 퀵 정렬 (1000개): {end_time - start_time:.4f}초")
    
    # 제자리 퀵 정렬
    start_time = time.time()
    quick_sort_in_place(large_data.copy())
    end_time = time.time()
    print(f"제자리 퀵 정렬 (1000개): {end_time - start_time:.4f}초")
    
    # 다른 테스트 케이스
    print("\n=== 다른 테스트 케이스 ===")
    test_cases = [
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # 이미 정렬됨 (최악의 경우가 될 수 있음)
        [5, 4, 3, 2, 1],  # 역순 (최악의 경우가 될 수 있음)
        [3, 3, 3, 3, 3],  # 모든 값이 같음
        [42],             # 원소 1개
        [],               # 빈 배열
    ]
    
    for i, data in enumerate(test_cases):
        original = data.copy()
        result = quick_sort(data.copy())
        print(f"테스트 {i + 1}: {original} -> {result}")
