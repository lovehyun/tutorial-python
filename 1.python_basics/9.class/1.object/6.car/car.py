class Car:
    def __init__(self, make, model):
        self._make = make
        self._model = model
        self._odometer = 0
    
    def get_descriptive_name(self):
        long_name = f"{self._make} {self._model}"
        return long_name.title()
    
    def read_odometer(self):
        print(f"This car has {self._odometer} miles on it.")
    
    def update_odometer(self, mileage):
        if mileage >= self._odometer:
            self._odometer = mileage
        else:
            print("You can't roll back an odometer!")
    
    def increment_odometer(self, distance):
        self._odometer += distance
