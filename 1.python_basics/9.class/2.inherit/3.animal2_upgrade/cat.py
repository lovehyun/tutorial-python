from animal import Animal

class Cat(Animal):
    # def __init__(self, name: str):
        # super().__init__(name, "Meow")
    def __init__(self, name: str, energy: int = 100) -> None:
        super().__init__(name, "Meow", energy)
        

    def move(self) -> None:
        if self.energy > 0:
            self.energy -= 10
            print(f"{self.name} is walking gracefully. Energy: {self.energy}")
        else:
            print(f"{self.name} is too tired to move.")
