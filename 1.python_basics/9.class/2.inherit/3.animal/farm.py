from animal import Animal

class Farm:
    def __init__(self):
        self._animals = []

    def add_animal(self, animal: Animal) -> None:
        self._animals.append(animal)
        print(f"{animal._name} has been added to the farm.")

    def feed_all(self) -> None:
        for animal in self._animals:
            animal.feed("Food")

    def play_all(self) -> None:
        for animal in self._animals:
            animal.move()

    def show_all(self) -> None:
        for animal in self._animals:
            print(f"Name: {animal.name}, Energy: {animal.energy}")
            animal.speak()
