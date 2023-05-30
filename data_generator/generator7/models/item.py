class Item:
    def __init__(self, name, type, unit_price):
        self.name = name
        self.type = type
        self.unit_price = unit_price

    def __str__(self):
        return f"Name: {self.name}, Type: {self.type}, Unit Price: {self.unit_price}"
