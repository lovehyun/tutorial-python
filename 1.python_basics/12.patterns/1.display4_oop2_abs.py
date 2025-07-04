#  각 객체에 display 메서드 추가 (OOP 정석)
class Dog:
    def display(self):
        print("강아지 객체 처리")

class Cat:
    def display(self):
        print("고양이 객체 처리")

class Human:
    def display(self):
        print("사람 객체 처리")

class DisplayData:
    def __init__(self, data):
        data.display()
        
DisplayData(Dog())    # 강아지 객체 처리
DisplayData(Cat())    # 고양이 객체 처리
DisplayData(Human())  # 사람 객체 처리

# DisplayData 가 없으면??
Dog().display()
Cat().display()


# 위 코드: "느슨한 OOP"
# - 파이썬의 덕 타이핑 (타입 신경 안 씀)
# - display 메서드가 없으면 런타임에서 AttributeError 발생
# - 코드 작성자는 display 메서드가 반드시 있다고 믿고 작성하는 구조 (강제는 없음)

#--------------------------------------------------------------------
# 아래 코드: "OOP 정석"
# - 추상 클래스 상속을 통해 display 메서드 구현을 강제
# - 만약 display 메서드가 없으면 코드 실행 전에 에러 발생
# - DisplayData2는 오직 Displayable을 상속한 객체만 받을 수 있음 (타입 안정성 확보)

from abc import ABC, abstractmethod

class Displayable(ABC):
    @abstractmethod
    def display(self):
        pass

class Dog2(Displayable):
    def display(self):
        print("강아지 객체 처리")

class Cat2(Displayable):
    def display(self):
        print("고양이 객체 처리")

class Human2(Displayable):
    def display(self):
        print("사람 객체 처리")

class DisplayData2:
    def __init__(self, data: Displayable):  # 타입 강제
        data.display()

DisplayData2(Dog())    # 강아지 객체 처리
DisplayData2(Cat())    # 고양이 객체 처리
DisplayData2(Human())  # 사람 객체 처리
