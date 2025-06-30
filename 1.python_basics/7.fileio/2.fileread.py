# 1. 파일 읽기
file_path = "file.txt"
file = open(file_path, "r")  # 파일 열기

contents = file.read()  # 파일 내용 읽기

file.close()  # 파일 닫기 (직접 닫아야 함)


# 2. 파일 읽기 (자동 닫기)
file_path = "file.txt"
with open(file_path, "r") as file:
# with open(file_path, "r", encoding="utf-8") as file:
    contents = file.read()
    
print("파일 내용:\n", contents)


# 3. 행 단위로 파일 읽기
file_path = "file.txt"
with open(file_path, "r") as file:
    lines = file.readlines()

print("파일 내용:")
for line in lines:
    print(line.strip())
