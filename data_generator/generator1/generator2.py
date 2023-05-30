import csv
import random

class NameGenerator:
    def __init__(self, file_path):
        self.names = self.load_data(file_path)

    def load_data(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().splitlines()
        return data

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
    def __init__(self, file_path):
        self.cities = self.load_data(file_path)

    def load_data(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().splitlines()
        return data

    def generate_address(self):
        city = random.choice(self.cities)
        street = random.randint(1, 100)
        return f"{street} {city}"

class DataGenerator:
    def __init__(self, name_file, city_file):
        self.name_gen = NameGenerator(name_file)
        self.birthdate_gen = BirthdateGenerator()
        self.gender_gen = GenderGenerator()
        self.address_gen = AddressGenerator(city_file)

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
            print(f"Name: {name}\nBirthdate: {birthdate}\nGender: {gender}\nAddress: {address}\n")

class DataExporter(DataGenerator):
    def export_to_csv(self, count, filename):
        data = self.generate_data(count)
        headers = ['Name', 'Birthdate', 'Gender', 'Address']
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)

# 프로그램 실행
name_file = 'names.txt'  # 이름 데이터 파일 경로
city_file = 'cities.txt'  # 도시 데이터 파일 경로

printer = DataPrinter(name_file, city_file)
exporter = DataExporter(name_file, city_file)

# 데이터 출력
printer.print_data(100)  # 100개의 데이터 출력

# CSV 파일로 저장
exporter.export_to_csv(100, 'data.csv')  # 100개의 데이터를 'data.csv' 파일로 저장
