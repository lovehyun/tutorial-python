from animal import Animal

class Dog(Animal):
    def speak(self) -> None:
        print(f"{self._name} says: Woof!")

    def move(self) -> None:
        # if self.energy <= 0:
        #     print(f"{self.name} is too tired to move!")
        #     return  # 체력이 없으면 이동 중단
        
        self._energy -= 10
        print(f"{self._name} is running. Energy: {self._energy}")
