# 1. 리스트 생성 및 기본 연산
# 리스트 생성
my_list = [1, 2, 3, 4, 5]

# 리스트 출력
print(my_list)  # [1, 2, 3, 4, 5]

# 리스트 길이 확인
print(len(my_list))  # 5

# 리스트 인덱싱
print(my_list[0])  # 1
print(my_list[-1])  # 5

# 리스트 슬라이싱
print(my_list[1:3])  # [2, 3]
print(my_list[:2])  # [1, 2]
print(my_list[3:])  # [4, 5]


# 2. 리스트 추가 및 확장
# 요소 추가
my_list.append(6)
print(my_list)  # [1, 2, 3, 4, 5, 6]

# 특정 위치에 요소 삽입
my_list.insert(2, 99)
print(my_list)  # [1, 2, 99, 3, 4, 5, 6]

# 다른 리스트 병합
another_list = [7, 8, 9]
my_list.extend(another_list)
print(my_list)  # [1, 2, 99, 3, 4, 5, 6, 7, 8, 9]

# 요소 추가 (연산자 사용)
my_list += [10, 11]
print(my_list)  # [1, 2, 99, 3, 4, 5, 6, 7, 8, 9, 10, 11]


# 3. 요소 제거
# 특정 요소 제거
my_list.remove(99)
print(my_list)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# 인덱스로 요소 제거
removed_element = my_list.pop(3)
print(removed_element)  # 4
print(my_list)  # [1, 2, 3, 5, 6, 7, 8, 9, 10, 11]

# 마지막 요소 제거
last_element = my_list.pop()
print(last_element)  # 11
print(my_list)  # [1, 2, 3, 5, 6, 7, 8, 9, 10]

# 모든 요소 제거
my_list.clear()
print(my_list)  # []


# 4. 검색 및 기타 유용한 메서드
my_list = [1, 2, 3, 4, 5, 3, 2, 1]

# 특정 값의 인덱스 찾기
index_of_3 = my_list.index(3)
print(index_of_3)  # 2

# 특정 값의 개수 세기
count_of_2 = my_list.count(2)
print(count_of_2)  # 2

# 리스트 정렬
my_list.sort()
print(my_list)  # [1, 1, 2, 2, 3, 3, 4, 5]

# 리스트 내림차순 정렬
my_list.sort(reverse=True)
print(my_list)  # [5, 4, 3, 3, 2, 2, 1, 1]

# 리스트 뒤집기
my_list.reverse()
print(my_list)  # [1, 1, 2, 2, 3, 3, 4, 5]

# 리스트 복사
copied_list = my_list.copy()
print(copied_list)  # [1, 1, 2, 2, 3, 3, 4, 5]


# 5. 리스트 컴프리헨션
# 0부터 9까지의 숫자 리스트 생성
numbers = [x for x in range(10)]
print(numbers)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

numbers = [x for x in range(1,5)]
print(numbers)  # [1, 2, 3, 4]

# 제곱 리스트 생성
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 조건을 이용한 리스트 생성
even_numbers = [x for x in range(10) if x % 2 == 0]
print(even_numbers)  # [0, 2, 4, 6, 8]


# 6. 기타 고급 함수
# 리스트 합치기
list1 = [1, 2, 3]
list2 = [4, 5, 6]
merged_list = list1 + list2
print(merged_list)  # [1, 2, 3, 4, 5, 6]

# 리스트 반복
repeated_list = [1, 2, 3] * 3
print(repeated_list)  # [1, 2, 3, 1, 2, 3, 1, 2, 3]

# 리스트 필터링 (filter와 lambda 함수)
filtered_list = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]))
print(filtered_list)  # [2, 4, 6]