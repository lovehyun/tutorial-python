# 기본 생성자
# 메서드

# 객체가 담고 있는 정보
# 요소	                설명
# 속성 (Attributes)	    객체가 저장하는 데이터 (변수)
# 메서드 (Methods)	    객체가 실행할 수 있는 동작 (함수)

class Person:
    def __init__(self, name, age):
        self.name = name  # 속성 (데이터 저장)
        self.age = age
        
    def greet(self):  # 메서드 (동작)
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def ride_car(self, car):
        print(f"{self.name} is riding the {car.make} {car.model}.")

if __name__ == "__main__":
    # Person 클래스의 인스턴스 생성
    person1 = Person("Alice", 30)
    person2 = Person("Bob", 25)

    # 메서드 호출
    person1.greet()
    person2.greet()


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
