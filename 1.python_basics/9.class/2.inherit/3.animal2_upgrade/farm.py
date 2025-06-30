from typing import List
from animal import Animal

class Farm:
    def __init__(self) -> None:
        self.animals: List[Animal] = []

    def add_animal(self, animal: Animal) -> None:
        self.animals.append(animal)
        print(f"{animal.name} has been added to the farm.")

    def all_speak(self) -> None:
        print("\nAll animals are speaking:")
        for animal in self.animals:
            animal.speak()

    def all_move(self) -> None:
        print("\nAll animals are moving:")
        for animal in self.animals:
            animal.move()

    def feed_all(self) -> None:
        print("\nFeeding all animals:")
        for animal in self.animals:
            animal.feed("Food")
