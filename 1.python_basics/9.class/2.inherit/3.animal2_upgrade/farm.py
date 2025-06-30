from typing import List
from animal import Animal

class Farm:
    def __init__(self) -> None:
        self.animals: List[Animal] = []
        # has-a는 "어떤 객체가 다른 객체를 속성으로 가진다"는 의미입니다.
        # 즉, "가지고 있다" → 포함하고 있다는 구조예요.

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
