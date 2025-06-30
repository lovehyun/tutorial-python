from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str):
        self.name = name
        self.hunger = 50  # 0 ~ 100
        self.energy = 50  # 0 ~ 100

    @abstractmethod
    def speak(self) -> None:
        pass

    @abstractmethod
    def move(self) -> None:
        pass

    def feed(self, food: str) -> None:
        self.hunger -= 10
        if self.hunger < 0:
            self.hunger = 0
        print(f"{self.name} ate {food}. Hunger: {self.hunger}")
