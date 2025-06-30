from typing import Optional
from person import Person
from car import Car

class Driver(Person):
    def __init__(self, name: str, age: int, license_type: str, car: Optional[Car] = None) -> None:
        super().__init__(name, age)
        self.license_type: str = license_type
        self.car: Optional[Car] = car  # Car or None

    def assign_car(self, car: Car) -> None:
        self.car = car
        print(f"{self.name} now owns a {car.get_descriptive_name()}.")

    def drive(self, distance: int) -> None:
        if self.car:
            print(f"{self.name} is driving the {self.car.get_descriptive_name()} for {distance} miles.")
            self.car.increment_odometer(distance)
            self.car.read_odometer()
        else:
            print(f"{self.name} has no car to drive.")
