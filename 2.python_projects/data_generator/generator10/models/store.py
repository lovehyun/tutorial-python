from models.basemodel import BaseModel, check_model_implementation


class Store(BaseModel):
    def __init__(self, id, name, store_type, address):
        self.id = id
        self.name = name
        self.store_type = store_type
        self.address = address

    def print_data(self):
        print(f"Id: {self.id}")
        print(f"Name: {self.name}")
        print(f"Type: {self.store_type}")
        print(f"Address: {self.address}")
        print()

    def get_row(self):
        return [self.id, self.name, self.store_type, self.address]

    @staticmethod
    def get_csv_filename():
        return "store.csv"

    @staticmethod
    def get_csv_header():
        return ['Id', 'Name', 'Type', 'Address']

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Type: {self.store_type}, Address: {self.address}"

check_model_implementation(Store)
