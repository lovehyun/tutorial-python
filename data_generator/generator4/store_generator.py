import random
from generators.address_generator import AddressGenerator

class Store:
    def __init__(self, name, store_type, address):
        self.name = name
        self.store_type = store_type
        self.address = address

class StoreGenerator(AddressGenerator):
    def __init__(self):
        super().__init__()
        self.store_types = ["스타벅스", "투썸", "이디야", "커피빈"]
        self.dongs = ['강남', '강서', '서초', '잠실', '신촌', '홍대', '송파']

    def generate_type(self):
        return random.choice(self.store_types)

    def generate_district(self):
        return random.choice(self.dongs)

    def generate_name(self, type):
        district = self.generate_district()
        store_number = random.randint(1, 10)
        return f"{type} {district}{store_number}호점"

    def generate(self):
        store_type = self.generate_type()
        name = self.generate_name(store_type)
        address = super().generate() # 상속받은 AddressGenerator 의 generate()
        return Store(name, store_type, address)

if __name__ == "__main__":
    store_gen = StoreGenerator()
    store = store_gen.generate()
    print(f"Name: {store.name}")
    print(f"Type: {store.store_type}")
    print(f"Address: {store.address}")
