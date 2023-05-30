import sys

from generators.user.user_generator import UserGenerator
from generators.store.store_generator import StoreGenerator
from generators.item.item_generator import ItemGenerator
# generators.order.order_generator = OrderGenerator()  # 새로운 데이터 생성 클래스 유형
from output import print_data


class DataGenerator:
    def __init__(self):
        self.user_gen = UserGenerator()
        self.store_gen = StoreGenerator()
        self.item_gen = ItemGenerator()
        # self.order_gen = OrderGenerator()  # 새로운 유형이 추가되면 여기에도?

    def generate_data(self, data_type, num_records):
        if data_type == "user":
            data = [self.user_gen.generate() for _ in range(num_records)]
        elif data_type == "store":
            data = [self.store_gen.generate() for _ in range(num_records)]
        elif data_type == "item":
            data = [self.item_gen.generate() for _ in range(num_records)]
        # 새로운 유형이 추가되면 여기에도? 여전히 복붙의 반복...
        # elif data_type == "order":
        #     data = [self.order_gen.generate() for _ in range(num_records)]
        else:
            print("지원되지 않는 데이터 유형입니다.")
            sys.exit(1)

        return data

def output_data(data, output_format):
    if output_format == "stdout":
        print_data(data, 'stdout')
    elif output_format == "csv":
        print_data(data, 'csv')
    elif output_format == "console":
        print_data(data, 'console')
    else:
        print("지원되지 않는 아웃풋 형태입니다.")
        sys.exit(1)


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

    gen_data = DataGenerator()

    data = gen_data.generate_data(data_type, num_records)
    output_data(data, output_format)
