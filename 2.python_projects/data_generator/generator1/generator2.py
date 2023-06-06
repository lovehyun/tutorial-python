import random

class NameGenerator:
    def __init__(self):
        self.names = ['John', 'Jane', 'Michael', 'Emily', 'William', 'Olivia']

    def generate_name(self):
        return random.choice(self.names)

class BirthdateGenerator:
    def generate_birthdate(self):
        year = random.randint(1970, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"

class GenderGenerator:
    def generate_gender(self):
        return random.choice(['Male', 'Female'])

class AddressGenerator:
    def __init__(self):
        self.cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia']

    def generate_address(self):
        city = random.choice(self.cities)
        street = random.randint(1, 100)
        return f"{street} {city}"

class DataGenerator:
    def __init__(self):
        self.name_gen = NameGenerator()
        self.birthdate_gen = BirthdateGenerator()
        self.gender_gen = GenderGenerator()
        self.address_gen = AddressGenerator()

    def generate_data(self, count):
        data = []
        for _ in range(count):
            name = self.name_gen.generate_name()
            birthdate = self.birthdate_gen.generate_birthdate()
            gender = self.gender_gen.generate_gender()
            address = self.address_gen.generate_address()
            data.append((name, birthdate, gender, address))
        return data

class DataPrinter(DataGenerator):
    def print_data(self, count):
        data = self.generate_data(count)
        for name, birthdate, gender, address in data:
            # print(f"Name: {name}, Birthdate: {birthdate}, Gender: {gender}, Address: {address}")
            print(f"Name: {name}\nBirthdate: {birthdate}\nGender: {gender}\nAddress: {address}\n")


# 프로그램 실행
printer = DataPrinter()

# 데이터 출력
printer.print_data(100)  # 100개의 데이터 출력
