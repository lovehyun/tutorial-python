# 객체지향 4대 특징을 모두 만족
#
# OOP 특징	    코드에서 적용된 부분
# 추상화	    Animal 추상 클래스, @abstractmethod
# 상속	        Dog와 Cat이 Animal을 상속
# 다형성	    animal.speak()가 동물마다 다르게 동작
# 캡슐화	    _name을 @property로 관리 (직접 접근 방지)

from abc import ABC, abstractmethod

class Animal(ABC):
    move_energy = 0  # 각 동물별 이동 시 소모 에너지 (자식 클래스가 override)
    
    # def __init__(self, name: str, sound: str):
    #     self.name = name
    #     self.sound = sound
    #     self.energy = 100  # 시작 에너지
    
    def __init__(self, name: str, sound: str, energy: int = 100) -> None:
        self._name = name
        self._sound = sound
        self._energy = energy  # 기본값 100, 직접 주면 변경 가능
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def energy(self) -> int:
        return self._energy
    
    @energy.setter
    def energy(self, value) -> None:
        if value >= 0 and value <= 100:
            self._energy = value
        else:
            print("에너지는 0 ~ 100 까지만 설정 할 수 있습니다.")
    
    def speak(self) -> None:
        print(self.speak_style())
        self._energy -= 10  # 짖을 때마다 에너지 감소

    def speak_style(self) -> str:
        if self._energy >= 80:
            return self._sound.upper()
        elif self._energy >= 50:
            return self._sound.capitalize()
        elif self._energy >= 20:
            return self._sound.lower()
        else:
            return "..."

    @abstractmethod
    def move(self) -> None:
        pass
    
    # def move(self) -> None:  # 공통 move 함수
    #     if self.energy > 0:
    #         self.energy -= type(self).move_energy
    #         print(f"{self.name} is moving. Energy: {self.energy}")
    #     else:
    #         print(f"{self.name} is too tired to move.")

    def feed(self, food: str) -> None:
        self._energy += 20
        if self._energy > 100:
            self._energy = 100
        print(f"{self._name} ate {food}. Energy: {self._energy}")
