import random

from generators.generator import Generator


class GenderGenerator(Generator):
    def generate(self):
        # 성별 생성 로직 구현
        genders = ['Male', 'Female']
        return random.choice(genders)
