import sys

from generators.user.user_generator import UserGenerator
from generators.store.store_generator import StoreGenerator
from output import save_to_csv, print_to_console, print_to_stdout


def generate_user(num_records):
    user_gen = UserGenerator()

    users = []
    for _ in range(num_records):
        user = user_gen.generate()
        users.append(user)

    return users

def generate_store(num_records):
    store_gen = StoreGenerator()

    stores = []
    for _ in range(num_records):
        store = store_gen.generate()
        stores.append(store)

    return stores

def simple_test():
    # User generation
    user_gen = UserGenerator()
    user = user_gen.generate()
    print("User:")
    print(f"Name: {user.name}")
    print(f"Gender: {user.gender}")
    print(f"Birthdate: {user.birthdate}")
    print(f"Address: {user.address}")
    # print("User 객체 출력: ", user)
    print()

    # Store generation
    store_gen = StoreGenerator()
    store = store_gen.generate()
    print("Store:")
    print(f"Name: {store.name}")
    print(f"Type: {store.store_type}")
    print(f"Address: {store.address}")
    # print("Store 객체 출력: ", store)


if __name__ == "__main__":
    # 명령줄에서 실행할 때 입력한 인자를 받음
    if len(sys.argv) > 3:
        data_type = sys.argv[1].lower()
        num_records = int(sys.argv[2])
        output_format = sys.argv[3].lower()
    else:
        data_type = input("데이터 유형을 입력하세요 (User 또는 Store): ").lower()
        num_records = int(input("생성할 데이터 개수를 입력하세요: "))
        output_format = input("아웃풋 형태를 입력하세요 (stdout, csv, console): ").lower()

    if data_type == "user":
        data = generate_user(num_records)
    elif data_type == "store":
        data = generate_store(num_records)
    else:
        print("지원되지 않는 데이터 유형입니다.")
        sys.exit(1)

    if output_format == "stdout":
        print_to_stdout(data)
    elif output_format == "csv":
        save_to_csv(data)
    elif output_format == "console":
        print_to_console(data)
    else:
        print("지원되지 않는 아웃풋 형태입니다.")
        sys.exit(1)
