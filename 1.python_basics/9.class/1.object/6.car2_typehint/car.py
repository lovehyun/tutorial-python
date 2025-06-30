class Car:
    def __init__(self, make: str, model: str) -> None:
        self.make: str = make
        self.model: str = model
        self.odometer_reading: int = 0

    def get_descriptive_name(self) -> str:
        return f"{self.make} {self.model}".title()

    def read_odometer(self) -> None:
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage: int) -> None:
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")

    def increment_odometer(self, miles: int) -> None:
        self.odometer_reading += miles

    # __repr__은 보통 개발자/디버깅용 표현을 리턴합니다.
    # __str__이 없으면 print(객체) 시 __repr__이 대신 호출됩니다.
    # 둘 다 정의하면 __str__이 우선 호출됩니다.

    def __repr__(self) -> str:
        return f"Car('{self.make}', '{self.model}')"
        
    def __str__(self) -> str:
        return f"Car: {self.make} {self.model}"


if __name__ == "__main__":
    car = Car("Hyundai", "Sonata")
    print(car)  # Car: Hyundai Sonata (자동으로 __str__ 호출)
