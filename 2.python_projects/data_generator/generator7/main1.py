import sys

from generators.user.user_generator import UserGenerator
from generators.store.store_generator import StoreGenerator
from generators.item.item_generator import ItemGenerator
from output import print_data


def generate_data(data_type, num_records):
    if data_type == "user":
        user_gen = UserGenerator()
        data = [user_gen.generate() for _ in range(num_records)]
    elif data_type == "store":
        store_gen = StoreGenerator()
        data = [store_gen.generate() for _ in range(num_records)]
    elif data_type == "item":
        item_gen = ItemGenerator()
        data = [item_gen.generate() for _ in range(num_records)]
    else:
        print("지원되지 않는 데이터 유형입니다.")
        sys.exit(1)

    return data


if __name__ == "__main__":
    # 명령줄에서 실행할 때 입력한 인자를 받음
    if len(sys.argv) > 3:
        data_type = sys.argv[1].lower()
        num_records = int(sys.argv[2])
        output_format = sys.argv[3].lower()
    else:
        data_type = input("데이터 유형을 입력하세요 (User, Store 또는 Item): ").lower()
        num_records = int(input("생성할 데이터 개수를 입력하세요: "))
        output_format = input("아웃풋 형태를 입력하세요 (stdout, csv, console): ").lower()

    data = generate_data(data_type, num_records)
    print_data(data, output_format)
