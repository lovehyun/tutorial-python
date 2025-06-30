# CSV 파일 읽기
import csv

file_path = "data.csv"

# 1. 리스트 형태로 읽기
with open(file_path, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)


# 2. 리스트에 담기
data = []
with open(file_path, "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    
    for row in csv_reader:
        data.append(row)  # 한 줄씩 추가

    
# 3. 딕셔너리 형태로 읽기
with open(file_path, "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # print(row)

        for row in csv_reader:
            data.append(row)  # row는 dict 형태

print(data)
