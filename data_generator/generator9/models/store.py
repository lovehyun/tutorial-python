class Store:
    def __init__(self, id, name, store_type, address):
        self.id = id
        self.name = name
        self.store_type = store_type
        self.address = address

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Type: {self.store_type}, Address: {self.address}"
