import sys

from generators.generator import DataGenerator
from output import print_data


if __name__ == "__main__":

    data_gen = DataGenerator()

    # 명령줄에서 실행할 때 입력한 인자를 받음
    if len(sys.argv) > 3:
        data_type = sys.argv[1].lower()
        num_records = int(sys.argv[2])
        output_format = sys.argv[3].lower()
    else:
        data_type = input("데이터 유형을 입력하세요 (User, Store 또는 Item): ").lower()
        num_records = int(input("생성할 데이터 개수를 입력하세요: "))
        output_format = input("아웃풋 형태를 입력하세요 (stdout, csv, console): ").lower()

    # 미션1. 버그를 의도적으로 추가하고, 디버깅 해보기
    # 미션2. 이 문제를 해결하기 위한 디자인 패턴 고민해보기
    # data_gen = DataGenerator()
    data = data_gen.generate_data(data_type, num_records)
    print_data(data, output_format)
