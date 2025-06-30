# 특징: 카드 게임하듯 하나씩 적절한 위치에 "삽입"
# 시간복잡도: 최악 O(n²), 최선 O(n)
# 장점: 작은 데이터나 거의 정렬된 데이터에서 빠름
# 단점: 큰 데이터에서는 느림

def insertion_sort(arr):
    """
    삽입 정렬 알고리즘
    카드를 정렬하듯이 각 원소를 적절한 위치에 삽입하는 방식
    """
    n = len(arr)
    
    # 두 번째 원소부터 시작 (첫 번째는 이미 정렬된 것으로 간주)
    for i in range(1, n):
        key = arr[i]  # 삽입할 원소
        j = i - 1     # 정렬된 부분의 마지막 인덱스
        
        # key보다 큰 원소들을 오른쪽으로 이동
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        # key를 적절한 위치에 삽입
        arr[j + 1] = key
    
    return arr

def insertion_sort_with_steps(arr):
    """
    삽입 정렬 과정을 단계별로 보여주는 버전
    """
    n = len(arr)
    total_compare_count = 0  # 총 비교 횟수
    print(f"초기 배열: {arr}")
    print(f"정렬된 부분: [{arr[0]}], 미정렬 부분: {arr[1:]}")
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        step_compare_count = 0  # 이번 단계의 비교 횟수

        print(f"\nStep {i}: 삽입할 원소 = {key}")
        print(f"정렬된 부분: {arr[:i]}")
        
        # key보다 큰 원소들을 오른쪽으로 이동
        while j >= 0:
            step_compare_count += 1
            total_compare_count += 1 # 비교할때마다 카운트 증가
            
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                # 삽입할 자리를 찾으면 비교 멈춤 (삽입 정렬의 최적화 포인트)
                break
        
        # key를 적절한 위치에 삽입
        arr[j + 1] = key
        
        print(f"결과: {arr}")
        print(f"정렬된 부분: {arr[:i+1]}, 미정렬 부분: {arr[i+1:]}")
        print(f"이번 단계 비교 횟수: {step_compare_count}회")

    print(f"\n총 비교 횟수: {total_compare_count}회")
    return arr

def insertion_sort_recursive(arr, n=None):
    """
    재귀적 삽입 정렬
    """
    if n is None:
        n = len(arr)
    
    # 기저 조건: 원소가 1개 이하면 이미 정렬됨
    if n <= 1:
        return arr
    
    # 먼저 n-1개 원소를 정렬
    insertion_sort_recursive(arr, n - 1)
    
    # 마지막 원소를 적절한 위치에 삽입
    last = arr[n - 1]
    j = n - 2
    
    while j >= 0 and arr[j] > last:
        arr[j + 1] = arr[j]
        j -= 1
    
    arr[j + 1] = last
    
    return arr

def binary_insertion_sort(arr):
    """
    이진 탐색을 이용한 삽입 정렬 (삽입 위치를 빠르게 찾기)
    """
    def binary_search(arr, val, start, end):
        """삽입할 위치를 이진 탐색으로 찾기"""
        if start == end:
            return start if arr[start] > val else start + 1
        
        if start > end:
            return start
        
        mid = (start + end) // 2
        
        if arr[mid] < val:
            return binary_search(arr, val, mid + 1, end)
        elif arr[mid] > val:
            return binary_search(arr, val, start, mid - 1)
        else:
            return mid
    
    for i in range(1, len(arr)):
        key = arr[i]
        # 이진 탐색으로 삽입 위치 찾기
        pos = binary_search(arr, key, 0, i - 1)
        
        # 원소들을 오른쪽으로 이동
        for j in range(i, pos, -1):
            arr[j] = arr[j - 1]
        
        # 적절한 위치에 삽입
        arr[pos] = key
    
    return arr

# 테스트 코드
if __name__ == "__main__":
    # 테스트 데이터
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print("=== 삽입 정렬 테스트 ===")
    print("원본 배열:", test_data)
    
    # 기본 삽입 정렬
    result1 = insertion_sort(test_data.copy())
    print("삽입 정렬 결과:", result1)
    
    print("\n=== 단계별 삽입 정렬 ===")
    result2 = insertion_sort_with_steps(test_data.copy())
    
    print("\n=== 재귀적 삽입 정렬 ===")
    result3 = insertion_sort_recursive(test_data.copy())
    print("재귀적 삽입 정렬 결과:", result3)
    
    print("\n=== 이진 탐색 삽입 정렬 ===")
    result4 = binary_insertion_sort(test_data.copy())
    print("이진 탐색 삽입 정렬 결과:", result4)
    
    # 다른 테스트 케이스
    print("\n=== 다른 테스트 케이스 ===")
    test_cases = [
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # 이미 정렬됨 (최선의 경우)
        [5, 4, 3, 2, 1],  # 역순 (최악의 경우)
        [3, 3, 3, 3, 3],  # 모든 값이 같음
        [42],             # 원소 1개
        [],               # 빈 배열
    ]
    
    for i, data in enumerate(test_cases):
        original = data.copy()
        result = insertion_sort(data.copy())
        print(f"테스트 {i + 1}: {original} -> {result}")
