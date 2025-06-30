from animal import Animal

class Cat(Animal):
    sound = "Meow"
    
    # def __init__(self, name: str):
    #   super().__init__(name, "Meow")
        
    def __init__(self, name: str, energy: int = 100) -> None:
        super().__init__(name, Cat.sound, energy)  # self.sound 보다 정석적으로는 클래스 변수인 Cat.sound 또는 type(self).sound 로 접근해야 함.
        
    # 고양이가 이동하는 동작: 에너지를 10씩 소모하며 달리는 행동
    def move(self) -> None:
        if self.energy > 0:
            self.energy -= 10
            print(f"{self.name} is walking gracefully. Energy: {self.energy}")
        else:
            print(f"{self.name} is too tired to move.")
