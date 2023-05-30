class User:
    def __init__(self, name, gender, birthdate, address):
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.address = address

    def __str__(self):
        return f"Name: {self.name}, Gender: {self.gender}, Birthdate: {self.birthdate}, Address: {self.address}"
