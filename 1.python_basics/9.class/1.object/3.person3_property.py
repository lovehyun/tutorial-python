# 구분	    전통적 방식	         @property 방식
# getter	get_name()	        person.name
# setter	set_name("Tom")	    person.name = "Tom"

class Person:
    def __init__(self, name, age):
        self._name = name    # protected (외부 접근은 가능하지만, 내부적으로 사용 권장)
        self._age = age
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value >= 0:
            self._age = value
        else:
            print("[Error] 나이는 0 이상이어야 합니다!")

    def greet(self):
        print(f"Hello, my name is {self._name} and I am {self._age} years old.")

if __name__ == "__main__":
    person = Person("Alice", 30)
    
    # getter처럼 사용
    print(person.name)
    print(person.age)

    # setter처럼 사용
    person.name = "Alicia"
    person.age = 35

    person.greet()

    # 잘못된 값 입력
    person.age = -5  # 경고 출력
