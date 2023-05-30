import csv

from models.user import User
from models.store import Store
from models.item import Item


def save_to_csv(data):
    if isinstance(data[0], User):  # 첫 번째 데이터가 User 객체인 경우
        filename = 'user.csv'
        header = ['Name', 'Birthdate', 'Gender', 'Address']
        rows = [[user.name, user.birthdate, user.gender, user.address] for user in data]
    elif isinstance(data[0], Store):  # 첫 번째 데이터가 Store 객체인 경우
        filename = 'store.csv'
        header = ['Name', 'Type', 'Address']
        rows = [[store.name, store.store_type, store.address] for store in data]
    elif isinstance(data[0], Item):  # 첫 번째 데이터가 Item 객체인 경우
        filename = 'item.csv'
        header = ['Name', 'Type', 'UnitPrice']
        rows = [[item.name, item.type, item.unit_price] for item in data]
    else:
        raise ValueError("Unsupported data type")

    with open(filename, 'w', newline='', encoding='euc-kr') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"데이터가 {filename} 파일로 저장되었습니다.")


def print_to_console(data):
    for item in data:
        if isinstance(item, User):
            print_user(item)
        elif isinstance(item, Store):
            print_store(item)
        elif isinstance(item, Item):
            print_item(item)
        else:
            print(f"Unknown data type: {type(item)}")

def print_user(user):
    print(f"Name: {user.name}")
    print(f"Birthdate: {user.birthdate}")
    print(f"Gender: {user.gender}")
    print(f"Address: {user.address}")
    print()

def print_store(store):
    print(f"Name: {store.name}")
    print(f"Type: {store.store_type}")
    print(f"Address: {store.address}")
    print()

def print_item(item):
    print(f"Name: {item.name}")
    print(f"Type: {item.type}")
    print(f"Unit Price: {item.unit_price}")
    print()


def print_to_stdout(data):
    for item in data:
        if isinstance(item, User):
            print(item)
        elif isinstance(item, Store):
            print(item)
        elif isinstance(item, Item):
            print(item)
        else:
            print(f"Unknown data type: {type(item)}")
