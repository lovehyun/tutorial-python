from models.basemodel import BaseModel, check_model_implementation


class Item(BaseModel):
    def __init__(self, id, name, type, unit_price):
        self.id = id
        self.name = name
        self.type = type
        self.unit_price = unit_price

    def print_data(self):
        print(f"Id: {self.id}")
        print(f"Name: {self.name}")
        print(f"Type: {self.type}")
        print(f"Unit Price: {self.unit_price}")
        print()

    def get_row(self):
        return [self.id, self.name, self.type, self.unit_price]

    @staticmethod
    def get_csv_filename():
        return "item.csv"

    @staticmethod
    def get_csv_header():
        return ['Id', 'Name', 'Type', 'UnitPrice']

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Type: {self.type}, Unit Price: {self.unit_price}"

check_model_implementation(Item)
