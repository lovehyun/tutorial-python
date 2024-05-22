# 1. 튜플 생성 및 기본 연산
# 튜플 생성
my_tuple = (1, 2, 3, 4, 5)

# 튜플 출력
print(my_tuple)  # (1, 2, 3, 4, 5)

# 튜플 길이 확인
print(len(my_tuple))  # 5

# 튜플 인덱싱
print(my_tuple[0])  # 1
print(my_tuple[-1])  # 5

# 튜플 슬라이싱
print(my_tuple[1:3])  # (2, 3)
print(my_tuple[:2])  # (1, 2)
print(my_tuple[3:])  # (4, 5)


# 2. 튜플 병합 및 반복
# 튜플 병합
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
merged_tuple = tuple1 + tuple2
print(merged_tuple)  # (1, 2, 3, 4, 5, 6)

# 튜플 반복
repeated_tuple = tuple1 * 3
print(repeated_tuple)  # (1, 2, 3, 1, 2, 3, 1, 2, 3)


# 3. 튜플 검색 및 기타 유용한 메서드
my_tuple = (1, 2, 3, 2, 1)

# 특정 값의 인덱스 찾기
index_of_3 = my_tuple.index(3)
print(index_of_3)  # 2

# 특정 값의 개수 세기
count_of_2 = my_tuple.count(2)
print(count_of_2)  # 2


# 4. 튜플 변환 및 활용
# 튜플은 불변이므로 변환 작업이 필요할 때 리스트로 변환 후 작업을 수행할 수 있습니다.

# 튜플을 리스트로 변환
my_list = list(my_tuple)
print(my_list)  # [1, 2, 3, 2, 1]

# 리스트를 튜플로 변환
new_tuple = tuple(my_list)
print(new_tuple)  # (1, 2, 3, 2, 1)


# 5. 튜플 언패킹
# 튜플은 한 번에 여러 변수를 할당하는 데 유용합니다.

# 튜플 언패킹
a, b, c = (1, 2, 3)
print(a)  # 1
print(b)  # 2
print(c)  # 3

# 튜플 언패킹을 사용한 다중 할당
my_tuple = (4, 5)
x, y = my_tuple
print(x)  # 4
print(y)  # 5


# 6. 튜플을 사용한 함수 반환값
# 함수에서 여러 값을 반환할 때 튜플을 사용합니다.
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)/len(numbers)

stats = get_stats([1, 2, 3, 4, 5])
print(stats)  # (1, 5, 3.0)

min_val, max_val, avg_val = get_stats([1, 2, 3, 4, 5])
print(min_val)  # 1
print(max_val)  # 5
print(avg_val)  # 3.0


# 7. 튜플 내포
# 리스트 컴프리헨션과 유사한 방법으로 튜플을 생성할 수는 없지만, 리스트 컴프리헨션을 사용한 후 이를 튜플로 변환할 수 있습니다.

# 튜플 내포 (리스트 컴프리헨션 후 변환)
squares = tuple(x**2 for x in range(10))
print(squares)  # (0, 1, 4, 9, 16, 25, 36, 49, 64, 81)


# 8. 네임드 튜플
# 네임드 튜플은 튜플에 이름을 부여하여 더 읽기 쉬운 코드를 작성할 수 있게 해줍니다.

from collections import namedtuple

# 네임드 튜플 정의
Point = namedtuple('Point', ['x', 'y'])

# 네임드 튜플 생성
p = Point(10, 20)
print(p)  # Point(x=10, y=20)

# 필드 접근
print(p.x)  # 10
print(p.y)  # 20
