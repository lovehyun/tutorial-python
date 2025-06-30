# CSV 파일 쓰기
import csv

file_path = "data.csv"

# 1. 리스트 데이터 저장
data = [
    ["Name", "Age", "City"],
    ["John", 25, "Seoul"],
    ["Jane", 30, "Busan"],
    ["Bob", 35, "Jeju"]
]
with open(file_path, "w", newline="") as file:
    csv_writer = csv.writer(file)
    # csv_writer.writerow(['Alice', 40, "Seoul"])
    csv_writer.writerows(data)

print("CSV 파일 쓰기 완료")


# 2. 딕셔너리 데이터 저장
data = [
    {"Name": "John", "Age": 25, "City": "Seoul"},
    {"Name": "Jane", "Age": 30, "City": "Busan"},
    {"Name": "Bob", "Age": 35, "City": "Jeju"}
]

for person in data:
    print(f"이름: {person['Name']}, 나이: {person['Age']}, 도시: {person['City']}")

# CSV 파일 쓰기
with open(file_path, "w", newline="") as file:
    # 헤더를 딕셔너리의 키 목록으로 설정
    headers = ["Name", "Age", "City"]
    # headers = data[0].keys()

    csv_writer = csv.DictWriter(file, fieldnames=headers)
    
    # 헤더 쓰기
    csv_writer.writeheader()
    
    # 딕셔너리 데이터를 CSV 파일에 쓰기
    csv_writer.writerows(data)
    
print("CSV 파일 쓰기 완료")
