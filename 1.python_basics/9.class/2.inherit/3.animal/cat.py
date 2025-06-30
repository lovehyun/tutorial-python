from animal import Animal

class Cat(Animal):
    def speak(self) -> None:
        print(f"{self.name} says: Meow!")

    def move(self) -> None:
        self.energy -= 5
        print(f"{self.name} is walking gracefully. Energy: {self.energy}")
