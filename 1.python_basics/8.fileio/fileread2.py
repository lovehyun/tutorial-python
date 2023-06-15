# 행 단위로 파일 읽기
file_path = "file.txt"
with open(file_path, "r") as file:
    lines = file.readlines()
print("파일 내용:")
for line in lines:
    print(line.strip())
