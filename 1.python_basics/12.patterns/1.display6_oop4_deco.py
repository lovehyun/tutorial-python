# OOP 정석
# decorator 기능을 통해서 구현
from abc import ABC, abstractmethod

class Displayable(ABC):
    registry = {}

    @classmethod
    def register(cls, obj_type):
        def decorator(subclass):
            cls.registry[obj_type] = subclass
            return subclass
        return decorator

    @abstractmethod
    def display(self):
        pass


@Displayable.register('dog')
class Dog(Displayable):
    def display(self):
        print("강아지 객체 처리")

@Displayable.register('cat')
class Cat(Displayable):
    def display(self):
        print("고양이 객체 처리")

@Displayable.register('human')
class Human(Displayable):
    def display(self):
        print("사람 객체 처리")


class Other():
    def display(self):
        print("기타 객체 처리")

class DisplayData3:
    def __init__(self, data_type: str):
        handler_class = Displayable.registry.get(data_type)
        if handler_class:
            handler = handler_class()
            handler.display()
        else:
            print("지원하지 않는 객체입니다.")


DisplayData3('dog')
DisplayData3('cat')
DisplayData3('human')
DisplayData3('fish')  # 지원하지 않는 객체입니다.
