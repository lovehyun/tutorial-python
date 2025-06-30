# 기능          문법                        설명
# 읽기 전용	    @property	                getter만 만들면 읽기 전용
# 읽고 쓰기	    @property + @속성.setter	getter + setter 함께 사용
# 삭제	        @속성.deleter	            del로 삭제 가능

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.deleter
    def name(self):
        print("이름이 삭제되었습니다.")
        self._name = None

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

    print(person.name)  # Alice 출력
    del person.name     # 이름 삭제
    print(person.name)  # None 출력
