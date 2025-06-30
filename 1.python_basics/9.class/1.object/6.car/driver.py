from person import Person
from car import Car

class Driver(Person):
    def __init__(self, name, age, license_type, car=None):
        super().__init__(name, age)
        self.license_type = license_type
        self.car = car  # Car 객체를 소유

    def assign_car(self, car):
        self.car = car
        print(f"{self.name} now owns a {car.get_descriptive_name()}.")

    def drive(self, distance):
        if self.car:
            print(f"{self.name} is driving the {self.car.get_descriptive_name()} for {distance} miles.")
            self.car.increment_odometer(distance)
            self.car.read_odometer()
        else:
            print(f"{self.name} has no car to drive.")
