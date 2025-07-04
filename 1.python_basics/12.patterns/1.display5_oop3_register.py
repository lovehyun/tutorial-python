# OOP 정석
# register 함수 기능 추가
from abc import ABC, abstractmethod

# __init_subclass__ 사용 → 자동 등록
# 상속만 하면 자동으로 레지스트리에 추가됨.
class Displayable(ABC):
    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Displayable.registry[cls] = cls

    @abstractmethod
    def display(self):
        pass


# 상속만 하면 자동으로 registry에 등록됨.
class Dog(Displayable):
    def display(self):
        print("강아지 객체 처리")

class Cat(Displayable):
    def display(self):
        print("고양이 객체 처리")

class Human(Displayable):
    def display(self):
        print("사람 객체 처리")

class Other():
    def display(self):
        print("기타 객체 처리")

class DisplayData3:
    def __init__(self, data: Displayable):
        handler = Displayable.registry.get(type(data))
        if handler:
            data.display()
        else:
            print("지원하지 않는 객체입니다.")


DisplayData3(Dog())    # 강아지 객체 처리
DisplayData3(Cat())    # 고양이 객체 처리
DisplayData3(Human())  # 사람 객체 처리
DisplayData3(Other())  # 사람 객체 처리
