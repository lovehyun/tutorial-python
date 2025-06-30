from dog import Dog
from cat import Cat
from farm import Farm

if __name__ == "__main__":
    farm = Farm()

    dog1 = Dog("Buddy")               # 기본 에너지 100
    cat1 = Cat("Kitty", energy=60)    # 초기 에너지 60
    dog2 = Dog("Charlie", 30)         # 초기 에너지 30

    farm.add_animal(dog1)
    farm.add_animal(cat1)
    farm.add_animal(dog2)

    # 여러 번 행동
    for _ in range(5):
        farm.all_speak()

    farm.all_move()

    # 에너지가 다 떨어지면 먹이 주기
    farm.feed_all()

    farm.all_speak()
