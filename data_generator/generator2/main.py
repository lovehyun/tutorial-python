from generators.name_generator import NameGenerator
from generators.birthdate_generator import BirthdateGenerator
from generators.gender_generator import GenderGenerator
from generators.address_generator import AddressGenerator

name_gen = NameGenerator()
name = name_gen.generate()

birthdate_gen = BirthdateGenerator()
birthdate = birthdate_gen.generate()

gender_gen = GenderGenerator()
gender = gender_gen.generate()

address_gen = AddressGenerator()
address = address_gen.generate()

print(f"Name: {name}")
print(f"Birthdate: {birthdate}")
print(f"Gender: {gender}")
print(f"Address: {address}")
