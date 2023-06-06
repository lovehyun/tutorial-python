import random


class StoreNameGenerator:
    def __init__(self):
        self.store_types = ["스타벅스", "투썸", "이디야", "커피빈"]
        self.dongs = ['강남', '강서', '서초', '잠실', '신촌', '홍대', '송파']

    def generate_type(self):
        return random.choice(self.store_types)

    def generate_district(self):
        return random.choice(self.dongs)

    def generate_name(self, store_type):
        district = self.generate_district()
        store_number = random.randint(1, 10)
        return f"{store_type} {district}{store_number}호점"
