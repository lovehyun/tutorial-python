from generators.generator import Generator
import random

class NameGenerator(Generator):
    def __init__(self):
        self.last_names = ['김', '이', '박', '최', '정']
        self.first_names = ['민준', '서연', '예준', '지우', '하윤']

    def generate(self):
        last_name = random.choice(self.last_names)
        first_name = random.choice(self.first_names)
        return last_name + first_name
