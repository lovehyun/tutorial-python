# 특징: 인접한 원소끼리 비교해서 큰 값을 뒤로 "거품처럼" 올려보냄
# 시간복잡도: O(n²), 최적화 시 최선의 경우 O(n)
# 장점: 구현이 가장 쉽고, 안정 정렬
# 단점: 가장 느림

def bubble_sort(arr):
    """
    버블 정렬 알고리즘
    인접한 두 원소를 비교하여 큰 값을 뒤로 보내는 방식
    """
    n = len(arr)
    
    # 전체 패스 (n-1번 반복)
    for i in range(n - 1):
        # 한 패스에서 인접한 원소들을 비교
        for j in range(n - 1 - i):
            # 앞의 원소가 뒤의 원소보다 크면 교환
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr

def bubble_sort_optimized(arr):
    """
    최적화된 버블 정렬 (조기 종료)
    """
    n = len(arr)
    
    for i in range(n - 1):
        swapped = False  # 교환이 발생했는지 확인
        
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # 교환이 없었다면 이미 정렬된 상태
        if not swapped:
            break
    
    return arr

# 테스트 코드
if __name__ == "__main__":
    # 테스트 데이터
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print("원본 배열:", test_data)
    
    # 기본 버블 정렬
    result1 = bubble_sort(test_data.copy())
    print("버블 정렬 결과:", result1)
    
    # 최적화된 버블 정렬
    result2 = bubble_sort_optimized(test_data.copy())
    print("최적화된 버블 정렬 결과:", result2)
    
    # 이미 정렬된 배열 테스트
    sorted_data = [1, 2, 3, 4, 5]
    print("\n이미 정렬된 배열:", sorted_data)
    result3 = bubble_sort_optimized(sorted_data.copy())
    print("최적화된 버블 정렬 결과:", result3)
