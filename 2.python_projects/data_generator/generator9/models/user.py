class User:
    def __init__(self, id, name, gender, birthdate, address):
        self.id = id
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.address = address

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Gender: {self.gender}, Birthdate: {self.birthdate}, Address: {self.address}"
