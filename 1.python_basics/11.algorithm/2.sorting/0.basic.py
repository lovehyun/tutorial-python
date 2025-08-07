def basic_sort(arr):
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                # Swap
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
                
                # arr[i], arr[j] = arr[j], arr[i]
    
    return arr

def basic_sort_with_count(arr):
    n = len(arr)
    compare_count = 0  # 비교 횟수 카운트
    
    for i in range(n):
        for j in range(i + 1, n):
            compare_count += 1  # 비교할 때마다 카운트
            print(f"\n[비교 {compare_count}회차] arr[{i}]={arr[i]} 와 arr[{j}]={arr[j]} 비교")

            if arr[i] > arr[j]:
                # Swap
                arr[i], arr[j] = arr[j], arr[i]
                print(f"-> 스왑 발생! 현재 배열: {arr}")
            else:
                print(f"-> 스왑 없음. 현재 배열: {arr}")
    
    print(f"\n총 비교 횟수: {compare_count}회")
    return arr

# 테스트
if __name__ == "__main__":
    data = [5, 3, 8, 4, 2]
    print("원본 배열:", data)
    
    sorted_data = basic_sort(data.copy())
    print("정렬 결과:", sorted_data)
    
    sorted_data = basic_sort_with_count(data.copy())
    print("정렬 결과:", sorted_data)
