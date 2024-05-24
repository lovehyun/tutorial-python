# CSV 파일 읽기
import csv

file_path = "data.csv"

# 1. 리스트 형태로 읽기
with open(file_path, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)


# 2. 딕셔너리 형태로 읽기
with open(file_path, "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        print(row)
