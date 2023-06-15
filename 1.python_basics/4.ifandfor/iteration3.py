# 0. 두 개의 2차원 리스트 생성
matrix1 = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]]

matrix2 = [[3, 4, 5],
           [6, 7, 8],
           [9, 10, 11]]


# ------------------------------
# 1. 두 배열의 중복되는 숫자 찾기 : 시간복잡도 O(n^4) 또는 
#    각각의 매트릭스에 따라 O(n^2 * m^2)
def find_duplicate_values(matrix1, matrix2):
    duplicate_values = []

    for row1 in matrix1:
        for row2 in matrix2:
            for value1 in row1:
                for value2 in row2:
                    if value1 == value2:
                        duplicate_values.append(value1)

    return duplicate_values

duplicates = find_duplicate_values(matrix1, matrix2)
print("Duplicate Values:", duplicates)


# ------------------------------
# 2. 매칭 시각화
def visualize_matching(matrix1, matrix2):
    duplicate_values = []

    for i, row1 in enumerate(matrix1):
        for j, row2 in enumerate(matrix2):
            for k, value1 in enumerate(row1):
                for l, value2 in enumerate(row2):
                    print(f"matrix1[{i}][{k}] == matrix2[{j}][{l}]", end="")
                    if value1 == value2:
                        duplicate_values.append(value1)
                        print(" match")
                    else:
                        print("")

# 매칭 순서 시각화
print("Matching Sequence:")
visualize_matching(matrix1, matrix2)


# ------------------------------
# 3. 베스트 솔루션
import numpy as np

# 두 개의 2차원 배열 생성
array1 = np.array(matrix1)
array2 = np.array(matrix2)

# 두 행렬에서 같은 요소 찾기 (시간복잡도 : O(NlogN))
duplicates = np.intersect1d(array1, array2)

# 결과 출력
print("Duplicate Values:", duplicates)


# ------------------------------
# 4. 베스트 솔루션 직접 구현

def flatten_matrix(matrix):
    flattened = []
    for row in matrix:
        flattened.extend(row)
    return flattened

def find_duplicate_values2(matrix1, matrix2):
    # 입력 배열을 정렬합니다.
    sorted_array1 = sorted(flatten_matrix(matrix1))
    sorted_array2 = sorted(flatten_matrix(matrix2))
    
    # 중복된 값을 저장할 리스트를 생성합니다.
    duplicate_values = []
    
    # 두 배열을 순회하면서 중복된 값을 찾습니다.
    i = 0
    j = 0
    while i < len(sorted_array1) and j < len(sorted_array2):
        if sorted_array1[i] == sorted_array2[j]:
            # 중복된 값이면 리스트에 추가합니다.
            duplicate_values.append(sorted_array1[i])
            i += 1
            j += 1
        elif sorted_array1[i] < sorted_array2[j]:
            i += 1
        else:
            j += 1
    
    return duplicate_values

duplicates = find_duplicate_values2(matrix1, matrix2)

# 결과 출력
print("Duplicate Values:", duplicates)
