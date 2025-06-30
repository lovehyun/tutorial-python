# typing 모듈: Python 3.5 부터 공식 지원 (List, Dict, Optional 등)
# 내장 타입 지원: Python 3.9
# | 연산자 지원: Python 3.10

class Person:
    def __init__(self, name: str, age: int) -> None:
        self._name: str = name
        self._age: int = age

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value) -> None:
        if value >= 0:
            self._age = value
        else:
            print("[Error] 나이는 0 이상이어야 합니다!")

    def greet(self) -> None:
        print(f"Hello, my name is {self._name} and I am {self._age} years old.")
