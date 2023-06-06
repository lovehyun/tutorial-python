from models.basemodel import BaseModel, check_model_implementation


class User(BaseModel):
    def __init__(self, id, name, gender, age, birthdate, address):
        self.id = id
        self.name = name
        self.gender = gender
        self.age = age
        self.birthdate = birthdate
        self.address = address

    def print_data(self):
        print(f"Id: {self.id}")
        print(f"Name: {self.name}")
        print(f"Gender: {self.gender}")
        print(f"Age: {self.age}")
        print(f"Birthdate: {self.birthdate}")
        print(f"Address: {self.address}")
        print()

    def get_row(self):
        return [self.id, self.name, self.gender, self.age, self.birthdate, self.address]

    @staticmethod
    def get_csv_filename():
        return "user.csv"

    @staticmethod
    def get_csv_header():
        return ['Id', 'Name', 'Gender', 'Age', 'Birthdate', 'Address']

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Gender: {self.gender}, Age: {self.age}, Birthdate: {self.birthdate}, Address: {self.address}"

check_model_implementation(User)
