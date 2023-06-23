import csv
import os


# 현재 파일의 디렉토리 경로
current_directory = os.path.dirname(os.path.abspath(__file__))

# CSV 파일 디렉토리 및 파일명 설정
csv_directory = os.path.join(current_directory, "../../")

"""
user_csv_filename = "user.csv"
store_csv_filename = "store.csv"

# UUID 데이터를 저장할 자료구조 초기화
user_uuids = []
store_uuids = []

# User CSV 파일 읽기
with open(f"{csv_directory}/{user_csv_filename}", "r") as file:
    reader = csv.reader(file)
    next(reader)  # 헤더 스킵
    for row in reader:
        user_uuids.append(row[0])  # UUID 컬럼에 해당하는 데이터 추출

# Store CSV 파일 읽기
with open(f"{csv_directory}/{store_csv_filename}", "r") as file:
    reader = csv.reader(file)
    next(reader)  # 헤더 스킵
    for row in reader:
        store_uuids.append(row[0])  # UUID 컬럼에 해당하는 데이터 추출
"""

def read_uuid_from_csv(csv_directory, csv_filename):
    uuids = []
    csv_path = os.path.join(csv_directory, csv_filename)

    if not os.path.isfile(csv_path):
        return uuids

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 스킵
        for row in reader:
            uuids.append(row[0])  # UUID 컬럼에 해당하는 데이터 추출

    return uuids


# UUID 데이터를 저장할 자료구조 초기화
user_uuids = read_uuid_from_csv(csv_directory, "user.csv")
store_uuids = read_uuid_from_csv(csv_directory, "store.csv")
item_uuids = read_uuid_from_csv(csv_directory, "item.csv")
order_uuids = read_uuid_from_csv(csv_directory, "order.csv")
