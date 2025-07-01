from person import Person
from car import Car

class Driver(Person):
    def __init__(self, name, age, license_type, car=None):
        super().__init__(name, age)
        self._license_type = license_type
        self._car = car  # Car 객체를 소유

    def assign_car(self, car):
        self._car = car
        print(f"{self.name} now owns a {car.get_descriptive_name()}.")

    def drive(self, distance):
        if self._car:
            print(f"{self.name} is driving the {self._car.get_descriptive_name()} for {distance} miles.")
            self._car.increment_odometer(distance)
            self._car.read_odometer()
        else:
            print(f"{self.name} has no car to drive.")
