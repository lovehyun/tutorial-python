import sys

from generators.user.user_generator import UserGenerator
from generators.store.store_generator import StoreGenerator
from generators.item.item_generator import ItemGenerator
from output import print_data


# Factory Pattern 을 사용해서 리펙토링
class DataGenerator:
    def __init__(self):
        self.generators = {}

    def register_generator(self, data_type, generator):
        self.generators[data_type] = generator
        
    def generate_data(self, data_type, num_records):
        if data_type not in self.generators:
            print("지원되지 않는 데이터 유형입니다.")
            sys.exit(1)

        generator = self.generators[data_type]
        data = [generator.generate() for _ in range(num_records)]  

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

    data_gen = DataGenerator()
    data_gen.register_generator("user", UserGenerator())
    data_gen.register_generator("store", StoreGenerator())
    data_gen.register_generator("item", ItemGenerator())

    data = data_gen.generate_data(data_type, num_records)
    output_data(data, output_format)
