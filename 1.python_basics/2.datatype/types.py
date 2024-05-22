# 1. type() 함수
# 사용법:
# type(object)

# 예시:
x = 5
y = "Hello"
z = [1, 2, 3]

# 변수의 타입 확인
print(type(x))  # <class 'int'>
print(type(y))  # <class 'str'>
print(type(z))  # <class 'list'>

# 객체의 타입 확인
print(type(5))  # <class 'int'>
print(type("Hello"))  # <class 'str'>
print(type([1, 2, 3]))  # <class 'list'>


# 2. isinstance() 함수
# 사용법:
# isinstance(object, classinfo)

# 예시:
x = 5
y = "Hello"
z = [1, 2, 3]

# 변수가 특정 클래스의 인스턴스인지 확인
print(isinstance(x, int))  # True
print(isinstance(y, str))  # True
print(isinstance(z, list))  # True

# 변수가 여러 클래스의 인스턴스인지 확인
print(isinstance(x, (int, float)))  # True
print(isinstance(y, (str, list)))  # True
print(isinstance(z, (str, list)))  # True

# 클래스 상속 관계에서의 사용
class A:
    pass

class B(A):
    pass

class C:
    pass

b = B()

print(isinstance(b, A))  # True
print(isinstance(b, B))  # True
print(isinstance(b, C))  # False
