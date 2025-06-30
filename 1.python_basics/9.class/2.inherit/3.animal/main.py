from farm import Farm
from cat import Cat
from dog import Dog

if __name__ == "__main__":
    farm = Farm()

    dog = Dog("Buddy")
    cat = Cat("Kitty")

    farm.add_animal(dog)
    farm.add_animal(cat)

    farm.show_all()
    farm.feed_all()
    farm.play_all()
