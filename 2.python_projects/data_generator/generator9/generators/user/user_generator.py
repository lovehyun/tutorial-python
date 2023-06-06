import uuid

from generators.generator import Generator, register_generator

from generators.user.name_generator import NameGenerator
from generators.user.gender_generator import GenderGenerator
from generators.user.birthdate_generator import BirthdateGenerator
from generators.common.address_generator import AddressGenerator

from models.user import User


@register_generator("user")
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
        user_id = uuid.uuid4()
        return User(user_id, name, gender, birthdate, address)
