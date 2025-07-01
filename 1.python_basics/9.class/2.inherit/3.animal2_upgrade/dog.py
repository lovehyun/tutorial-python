from animal import Animal

class Dog(Animal):
    sound = "Woof"  # 클래스 변수
    move_energy = 15  # 개는 이동 시 15 소모

    # def __init__(self, name: str):
    #   super().__init__(name, "Woof")
    
    def __init__(self, name: str, energy: int = 100) -> None:
        super().__init__(name, Dog.sound, energy)  # 정확한 접근 (클래스명.변수명)
        # super().__init__(name, type(self).sound, energy)  # 더 안전한 코드 (상속 확장성까지 고려)

    # 개가 이동하는 동작: 에너지를 15씩 소모하며 달리는 행동
    def move(self) -> None:
        if self.energy > 0:
            self._energy -= 15
            print(f"{self._name} is running. Energy: {self._energy}")
        else:
            print(f"{self._name} is too tired to move.")


# 상속시 문제란?
#
# class Dog(Animal):
#     sound = "Woof"
#
# class Puppy(Dog):
#     sound = "Yip"
#
# dog = Puppy("Buddy")
#
# type(self).sound → 'Yip' (자식 클래스의 소리)
# Dog.sound → 'Woof' (부모 클래스의 소리)
