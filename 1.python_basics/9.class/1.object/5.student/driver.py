from person import Person

class Driver(Person):
    def __init__(self, name, age, license_type):
        super().__init__(name, age)
        self.license_type = license_type

    def drive(self):
        print(f"{self.name} is driving with a {self.license_type} license.")
