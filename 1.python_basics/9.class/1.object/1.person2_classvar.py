# 기본 생성자
# 메서드

# 객체가 담고 있는 정보
# 요소	                설명
# 속성 (Attributes)	    객체가 저장하는 데이터 (변수)
# 메서드 (Methods)	    객체가 실행할 수 있는 동작 (함수)

class Person:
    count = 0  # 클래스 변수 (공용)
    
    def __init__(self, name, age):
        self.name = name  # 속성 (데이터 저장) - 인스턴스 변수 (객체마다 별도로 생성/저장됨)
        self.age = age
        Person.count += 1  # 클래스 변수는 이렇게 접근
        # type(self).count += 1  # 더 확장성 있는 코드 (상속에도 안전)

    def __str__(self):  # 사람이 읽기 좋게
        return f"Person(name={self.name}, age={self.age})"
    
    def __repr__(self):  # 개발자 디버깅용
        return f"Person('{self.name}', {self.age})"

    def __eq__(self, other):  # 객체 비교
        return self.name == other.name and self.age == other.age

    @classmethod
    def get_count(cls):
        return cls.count
    
    def greet(self):  # 메서드 (동작)
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def ride_car(self, car):
        print(f"{self.name} is riding the {car.make} {car.model}.")

if __name__ == "__main__":
    # Person 클래스의 인스턴스 생성
    person1 = Person("Alice", 30)
    person2 = Person("Bob", 25)
    person3 = Person("Alice", 30)

    # 메서드 호출
    person1.greet()
    person2.greet()

    print(person1)  # 자동으로 __str__ 호출
    print(person1 == person2)  # False
    print(person1 == person3)  # True
    
    # 파이썬은 모든 것이 객체이기 때문에, 클래스도 "정의되면 바로 메모리에 올라가는 실체"입니다.
    # 다른 언어와 다름. Java는 런타임에 객체가 생성됨. Python 은 클래스는 객체 (first-class object)
    print("현재 생성된 사람 수:", Person.count)
    print("현재 생성된 사람 수:", Person.get_count())
    print(person1.count)
    print(person2.count)

# 객체가 담는 것 요약
# person1 = {
#     'name': 'Alice',
#     'age': 30,
#     '__class__': Person,
#     '__dict__': {'name': 'Alice', 'age': 30}
# }
#
# print(person1.__dict__)   # {'name': 'Alice', 'age': 30}
# print(person1.__class__)  # <class '__main__.Person'>
# print(person1.__class__.__dict__)  # 클래스 내부 함수들 출력
# for name, value in person1.__class__.__dict__.items():
#     if callable(value):
#         print(f"{name}: {value}")
