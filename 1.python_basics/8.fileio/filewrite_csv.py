# CSV 파일 쓰기
import csv

file_path = "data.csv"
data = [
    ["Name", "Age", "City"],
    ["John", "25", "Seoul"],
    ["Jane", "30", "Busan"],
    ["Bob", "35", "Jeju"]
]
with open(file_path, "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)
print("CSV 파일 쓰기 완료")
