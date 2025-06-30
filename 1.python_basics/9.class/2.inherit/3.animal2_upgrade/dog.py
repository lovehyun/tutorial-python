from animal import Animal

class Dog(Animal):
    # def __init__(self, name: str):
        # super().__init__(name, "Woof")
    def __init__(self, name: str, energy: int = 100) -> None:
        super().__init__(name, "Woof", energy)

    def move(self) -> None:
        if self.energy > 0:
            self.energy -= 15
            print(f"{self.name} is running. Energy: {self.energy}")
        else:
            print(f"{self.name} is too tired to move.")
