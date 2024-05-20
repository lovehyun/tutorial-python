class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
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
