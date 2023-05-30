from generators.generator import Generator

from generators.user.name_generator import NameGenerator
from generators.user.gender_generator import GenderGenerator
from generators.user.birthdate_generator import BirthdateGenerator
from generators.common.address_generator import AddressGenerator

from models.user import User


class UserGenerator(Generator):
    def __init__(self):
        self.name_generator = NameGenerator()
        self.gender_generator = GenderGenerator()
        self.birthdate_generator = BirthdateGenerator()
        self.address_generator = AddressGenerator()

    def generate(self):
        name = self.name_generator.generate()
        gender = self.gender_generator.generate()
        birthdate = self.birthdate_generator.generate()
        address = self.address_generator.generate()
        return User(name, gender, birthdate, address)
