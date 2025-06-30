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
