class Store:
    def __init__(self, name, store_type, address):
        self.name = name
        self.store_type = store_type
        self.address = address

    def __str__(self):
        return f"Name: {self.name}, Type: {self.store_type}, Address: {self.address}"
