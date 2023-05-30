from generators.generator import Generator
import random

class NameGenerator(Generator):
    def generate(self):
        # 이름 생성 로직 구현
        names = ['John', 'Jane', 'Michael', 'Emily', 'William', 'Olivia']
        return random.choice(names)
