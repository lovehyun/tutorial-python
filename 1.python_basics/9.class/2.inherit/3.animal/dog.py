from animal import Animal

class Dog(Animal):
    def speak(self) -> None:
        print(f"{self.name} says: Woof!")

    def move(self) -> None:
        self.energy -= 10
        print(f"{self.name} is running. Energy: {self.energy}")
