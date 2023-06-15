# CSV 파일 읽기
import csv

file_path = "data.csv"
with open(file_path, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
