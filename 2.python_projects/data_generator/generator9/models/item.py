class Item:
    def __init__(self, id, name, type, unit_price):
        self.id = id
        self.name = name
        self.type = type
        self.unit_price = unit_price

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Type: {self.type}, Unit Price: {self.unit_price}"
