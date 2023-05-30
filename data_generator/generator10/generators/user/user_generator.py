import uuid
from datetime import datetime

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
        age = self._calculate_age(birthdate)  # 나이 계산
        address = self.address_generator.generate()
        user_id = uuid.uuid4()
        return User(user_id, name, gender, age, birthdate, address)

    def _calculate_age(self, birthdate):
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")  # 문자열을 datetime 객체로 변환
        today = datetime.today().date()
        age = today.year - birthdate.year
        if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
            age -= 1
        return age
