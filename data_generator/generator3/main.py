import sys
import csv

from generators.name_generator import NameGenerator
from generators.birthdate_generator import BirthdateGenerator
from generators.gender_generator import GenderGenerator
from generators.address_generator import AddressGenerator


def generate_data(num_records):
    name_gen = NameGenerator()
    birthdate_gen = BirthdateGenerator()
    gender_gen = GenderGenerator()
    address_gen = AddressGenerator()

    data = []
    for _ in range(num_records):
        name = name_gen.generate()
        birthdate = birthdate_gen.generate()
        gender = gender_gen.generate()
        address = address_gen.generate()

        data.append([name, birthdate, gender, address])

    return data

def save_to_csv(data):
    with open('output.csv', 'w', newline='', encoding='euc-kr') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Birthdate', 'Gender', 'Address'])
        writer.writerows(data)

def print_to_console(data):
    for row in data:
        print(f"Name: {row[0]}")
        print(f"Birthdate: {row[1]}")
        print(f"Gender: {row[2]}")
        print(f"Address: {row[3]}")
        print()

def print_to_stdout(data):
    for row in data:
        print(', '.join(row))

# 명령줄에서 실행할 때 입력한 인자를 받음
if len(sys.argv) > 1:
    num_records = int(sys.argv[1])
else:
    num_records = int(input("생성할 데이터 개수를 입력하세요: "))

output_format = "stdout"  # 기본 출력 포맷은 stdout으로 설정
if len(sys.argv) > 2:
    output_format = sys.argv[2]

data = generate_data(num_records)

if output_format == "console":
    print_to_console(data)
elif output_format == "csv":
    save_to_csv(data)
    print("데이터가 output.csv 파일로 저장되었습니다.")
else:
    print_to_stdout(data)
