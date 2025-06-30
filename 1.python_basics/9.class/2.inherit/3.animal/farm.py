from animal import Animal

class Farm:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal: Animal) -> None:
        self.animals.append(animal)
        print(f"{animal.name} has been added to the farm.")

    def feed_all(self) -> None:
        for animal in self.animals:
            animal.feed("Food")

    def play_all(self) -> None:
        for animal in self.animals:
            animal.move()

    def show_all(self) -> None:
        for animal in self.animals:
            animal.speak()
