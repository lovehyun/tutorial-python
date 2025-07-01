from typing import List
from animal import Animal

class Farm:
    def __init__(self) -> None:
        self._animals: List[Animal] = []
        # has-a는 "어떤 객체가 다른 객체를 속성으로 가진다"는 의미입니다.
        # 즉, "가지고 있다" → 포함하고 있다는 구조예요.

    def add_animal(self, animal: Animal) -> None:
        self._animals.append(animal)
        print(f"{animal._name} has been added to the farm.")

    def all_speak(self) -> None:
        print("\nAll animals are speaking:")
        for animal in self._animals:
            animal.speak()

    def all_move(self) -> None:
        print("\nAll animals are moving:")
        for animal in self._animals:
            animal.move()

    def feed_all(self) -> None:
        print("\nFeeding all animals:")
        for animal in self._animals:
            animal.feed("Food")

    def show_all(self) -> None:
        for animal in self._animals:
            print(f"Name: {animal.name}, Energy: {animal.energy}")
            animal.speak()
