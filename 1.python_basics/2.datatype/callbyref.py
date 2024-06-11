# Call by Value: 파이썬에서는 사용되지 않음.
# Call by Reference: 파이썬의 변수 전달 방식으로, 함수 내에서 가변 객체를 변경하면 원래 객체도 변경됨.
# Shallow Copy: 객체의 최상위 레벨만 복사, 내부 객체는 참조.
# Deep Copy: 객체와 모든 내부 객체를 재귀적으로 복사, 원래 객체와 독립된 새로운 객체 생성.

# 변수 및 참조 예시
a = [1, 2, 3]
b = a
b.append(4)

print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2, 3, 4]

print(id(a))  # 예: 139959029845392
print(id(b))  # 예: 139959029845392 - 동일한 객체 ID



# 불변 객체 (Immutable objects)
def modify_immutable(x):
    x = 10  # 새로운 객체를 할당
    print("Inside function:", x)

a = 5
modify_immutable(a)
print("Outside function:", a)  # a는 여전히 5


# 가변 객체 (Mutable objects)
def modify_mutable(lst):
    lst.append(4)  # 원래 객체를 변경

my_list = [1, 2, 3]
modify_mutable(my_list)
print(my_list)  # [1, 2, 3, 4]



# Shallow-copy 예시

import copy

a = [1, 2, 3]
b = copy.copy(a)  # 또는 b = a.copy()

b.append(4)
print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3, 4] - 독립적인 복사본


# 원본 객체 생성
original_list = [1, 2, [3, 4]]

# 얕은 복사 수행
shallow_copied_list = copy.copy(original_list)

# 내부 가변 객체 변경
shallow_copied_list[2][0] = 'a'

# 결과 출력
print("원본 리스트:", original_list)          # [1, 2, ['a', 4]]
print("얕은 복사된 리스트:", shallow_copied_list)  # [1, 2, ['a', 4]]


# Deep-copy 예시

a = [1, 2, [3, 4]]
b = copy.deepcopy(a)

b[2].append(5)
print(a)  # [1, 2, [3, 4]]
print(b)  # [1, 2, [3, 4, 5]] - 깊은 복사로 인해 완전히 독립적인 복사본
