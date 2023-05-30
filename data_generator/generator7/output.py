import csv

from models.user import User
from models.store import Store
from models.item import Item


def save_to_csv(data):
    data_type_info = {
        User: {
            'filename': 'user.csv',
            'header': ['Name', 'Birthdate', 'Gender', 'Address'],
            'get_row': lambda user: [user.name, user.birthdate, user.gender, user.address]
        },
        Store: {
            'filename': 'store.csv',
            'header': ['Name', 'Type', 'Address'],
            'get_row': lambda store: [store.name, store.store_type, store.address]
        },
        Item: {
            'filename': 'item.csv',
            'header': ['Name', 'Type', 'UnitPrice'],
            'get_row': lambda item: [item.name, item.type, item.unit_price]
        }
    }

    data_type = type(data[0])
    if data_type in data_type_info:
        info = data_type_info[data_type]
        filename = info['filename']
        header = info['header']
        rows = [info['get_row'](item) for item in data]
        with open(filename, 'w', newline='', encoding='euc-kr') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"데이터가 {filename} 파일로 저장되었습니다.")
    else:
        raise ValueError("Unsupported data type")


def print_data_item(item):
    if isinstance(item, User):
        print(f"Name: {item.name}")
        print(f"Birthdate: {item.birthdate}")
        print(f"Gender: {item.gender}")
        print(f"Address: {item.address}")
    elif isinstance(item, Store):
        print(f"Name: {item.name}")
        print(f"Type: {item.store_type}")
        print(f"Address: {item.address}")
    elif isinstance(item, Item):
        print(f"Name: {item.name}")
        print(f"Type: {item.type}")
        print(f"Unit Price: {item.unit_price}")
    else:
        print(f"Unknown data type: {type(item)}")
    print()


def print_data(data, output_format):
    if output_format == "stdout":
        for item in data:
            print(item)
    elif output_format == "console":
        for item in data:
            print_data_item(item)
    elif output_format == "csv":
        save_to_csv(data)
    else:
        print("지원되지 않는 아웃풋 형태입니다.")
