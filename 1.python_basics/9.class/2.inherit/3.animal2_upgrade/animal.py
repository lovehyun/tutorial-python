# 객체지향 4대 특징을 모두 만족
#
# OOP 특징	    코드에서 적용된 부분
# 추상화	    Animal 추상 클래스, @abstractmethod
# 상속	        Dog와 Cat이 Animal을 상속
# 다형성	    animal.speak()가 동물마다 다르게 동작
# 캡슐화	    _name을 @property로 관리 (직접 접근 방지)

from abc import ABC, abstractmethod

class Animal(ABC):
    # def __init__(self, name: str, sound: str):
    #     self.name = name
    #     self.sound = sound
    #     self.energy = 100  # 시작 에너지
    
    def __init__(self, name: str, sound: str, energy: int = 100) -> None:
        self.name = name
        self.sound = sound
        self.energy = energy  # 기본값 100, 직접 주면 변경 가능
        
    def speak(self) -> None:
        if self.energy < 20:
            print("...")
        else:
            print(self.speak_style())

        self.energy -= 10  # 짖을 때마다 에너지 감소

    def speak_style(self) -> str:
        if self.energy >= 80:
            return self.sound.upper()
        elif self.energy >= 50:
            return self.sound.capitalize()
        elif self.energy >= 20:
            return self.sound.lower()
        else:
            return "..."

    @abstractmethod
    def move(self) -> None:
        pass

    def feed(self, food: str) -> None:
        self.energy += 20
        if self.energy > 100:
            self.energy = 100
        print(f"{self.name} ate {food}. Energy: {self.energy}")
