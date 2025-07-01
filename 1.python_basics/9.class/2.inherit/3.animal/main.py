from farm import Farm
from cat import Cat
from dog import Dog

def play_animal():
    dog = Dog("Buddy")
    cat = Cat("Kitty")
    
    dog.speak()
    cat.speak()
    
    dog.move()
    cat.move()
    
    # 개 10번 이동
    for _ in range(10):
        dog.move()
        
    # 고양이 10번 이동
    for _ in range(10):
        cat.move()
        
    # # 리스트에 담기
    # animals = [dog, cat]
    
    # # 10번 반복
    # for _ in range(10):
    #     for animal in animals:
    #         animal.move()

def build_farm():
    farm = Farm()

    dog = Dog("Buddy")
    cat = Cat("Kitty")

    farm.add_animal(dog)
    farm.add_animal(cat)

    farm.show_all()
    farm.feed_all()
    farm.play_all()
    
    # 모든 동물 10번 반복 이동
    for _ in range(10):
        farm.play_all()

if __name__ == "__main__":
    play_animal()
