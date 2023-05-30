from generators.generator import Generator
import random

class AddressGenerator(Generator):
    def generate(self):
        # 주소 생성 로직 구현
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia']
        street = random.randint(1, 100)
        city = random.choice(cities)
        return f"{street} {city}"
