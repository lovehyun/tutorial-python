import csv

from models.user import User
from models.store import Store
from models.item import Item
from models.order import Order
from models.orderitem import OrderItem


def save_to_csv(data):
    data_type_info = {
        User: {
            'filename': 'user.csv',
            'header': ['Id', 'Name', 'Birthdate', 'Gender', 'Address'],
            'get_row': lambda user: [user.id, user.name, user.birthdate, user.gender, user.address]
        },
        Store: {
            'filename': 'store.csv',
            'header': ['Id', 'Name', 'Type', 'Address'],
            'get_row': lambda store: [store.id, store.name, store.store_type, store.address]
        },
        Item: {
            'filename': 'item.csv',
            'header': ['Id', 'Name', 'Type', 'UnitPrice'],
            'get_row': lambda item: [item.id, item.name, item.type, item.unit_price]
        },
        Order: {
            'filename': 'order.csv',
            'header': ['Id', 'OrderAt', 'StoreId', 'UserId'],
            'get_row': lambda order: [order.id, order.order_at, order.store_id, order.user_id]
        },
        OrderItem: {
            'filename': 'orderitem.csv',
            'header': ['Id', 'OrderId', 'ItemId'],
            'get_row': lambda orderitem: [orderitem.id, orderitem.order_id, orderitem.item_id]
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
    data_type_info = {
        User: ['Id', 'Name', 'Birthdate', 'Gender', 'Address'],
        Store: ['Id', 'Name', 'Type', 'Address'],
        Item: ['Id', 'Name', 'Type', 'Unit Price'],
        Order: ['Id', 'Order At', 'Store Id', 'User Id'],
        OrderItem: ['Id', 'Order Id', 'Item Id']
    }

    data_type = type(item)
    if data_type in data_type_info:
        fields = data_type_info[data_type]
        for field in fields:
            value = getattr(item, field.lower().replace(' ', '_'))
            print(f"{field}: {value}")
    else:
        print(f"Unknown data type: {data_type}")
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
