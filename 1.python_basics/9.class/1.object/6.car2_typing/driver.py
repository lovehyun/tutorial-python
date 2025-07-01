from typing import Optional
from person import Person
from car import Car

class Driver(Person):
    def __init__(self, name: str, age: int, license_type: str, car: Optional[Car] = None) -> None:
        super().__init__(name, age)
        self._license_type: str = license_type
        self._car: Optional[Car] = car  # Car or None

    def assign_car(self, car: Car) -> None:
        self._car = car
        print(f"{self.name} now owns a {car.get_descriptive_name()}.")

    def drive(self, distance: int) -> None:
        if self._car:
            print(f"{self.name} is driving the {self._car.get_descriptive_name()} for {distance} miles.")
            self._car.increment_odometer(distance)
            self._car.read_odometer()
        else:
            print(f"{self.name} has no car to drive.")
