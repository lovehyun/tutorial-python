from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str):
        self._name: str = name
        self._energy: int = 50  # 0 ~ 100

    @property
    def name(self) -> str:
        return self._name

    @property
    def energy(self) -> int:
        return self._energy
    
    @abstractmethod
    def speak(self) -> None:
        pass

    @abstractmethod
    def move(self) -> None:
        pass

    def feed(self, food: str) -> None:
        if self._energy < 100:
            self._energy += 50
        print(f"{self._name} ate {food}. Energy: {self._energy}")
