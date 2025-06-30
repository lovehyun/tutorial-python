# 특징: 매번 최소값(또는 최대값)을 "선택"해서 앞으로 보냄
# 시간복잡도: 항상 O(n²)
# 장점: 교환 횟수가 적음 (최대 n-1번)
# 단점: 이미 정렬된 배열도 똑같이 느림

def selection_sort(arr):
    """
    선택 정렬 알고리즘
    매번 최솟값을 찾아서 맨 앞으로 보내는 방식
    """
    n = len(arr)
    
    # 배열을 순회하면서 각 위치에 최솟값을 배치
    for i in range(n - 1):
        # 현재 위치를 최솟값 위치로 가정
        min_idx = i
        
        # 나머지 배열에서 최솟값 찾기
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # 최솟값을 현재 위치로 교환
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr

def selection_sort_with_steps(arr):
    """
    선택 정렬 과정을 단계별로 보여주는 버전
    """
    n = len(arr)
    compare_count = 0  # 비교 횟수 카운트
    print(f"초기 배열: {arr}")
    
    for i in range(n - 1):
        min_idx = i
        step_compare_count = 0  # 이번 단계의 비교 횟수
        
        # 최소값 찾기
        for j in range(i + 1, n):
            step_compare_count += 1
            compare_count += 1  # 비교할 때마다 증가
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # 교환
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            print(f"Step {i + 1}: {arr} (인덱스 {i} 기준. 최소값 {arr[i]}을 위치 {i}로 이동, 비교 {step_compare_count}회)")
        else:
            print(f"Step {i + 1}: {arr} (인덱스 {i} 기준. 이미 올바른 위치, 비교 {step_compare_count}회)")
    
    print(f"\n총 비교 횟수: {compare_count}회")
    return arr

def find_max_selection_sort(arr):
    """
    최대값을 찾아서 뒤로 보내는 선택 정렬 변형
    """
    n = len(arr)
    
    for i in range(n - 1, 0, -1):  # 뒤에서부터 시작
        # 최대값 찾기
        max_idx = 0
        for j in range(1, i + 1):
            if arr[j] > arr[max_idx]:
                max_idx = j
        
        # 최대값을 현재 위치(맨 뒤)로 교환
        if max_idx != i:
            arr[i], arr[max_idx] = arr[max_idx], arr[i]
    
    return arr

# 테스트 코드
if __name__ == "__main__":
    # 테스트 데이터
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print("=== 선택 정렬 테스트 ===")
    print("원본 배열:", test_data)
    
    # 기본 선택 정렬
    result1 = selection_sort(test_data.copy())
    print("선택 정렬 결과:", result1)
    
    print("\n=== 단계별 선택 정렬 ===")
    result2 = selection_sort_with_steps(test_data.copy())
    
    print("\n=== 최대값 기준 선택 정렬 ===")
    result3 = find_max_selection_sort(test_data.copy())
    print("최대값 기준 정렬 결과:", result3)
    
    # 다른 테스트 케이스
    print("\n=== 다른 테스트 케이스 ===")
    test_cases = [
        [5, 2, 8, 1, 9],
        [1, 2, 3, 4, 5],  # 이미 정렬됨
        [5, 4, 3, 2, 1],  # 역순
        [3, 3, 3, 3, 3],  # 모든 값이 같음
    ]
    
    for i, data in enumerate(test_cases):
        print(f"테스트 {i + 1}: {data} -> {selection_sort(data.copy())}")
