# 1. 파일 읽기
file_path = "file.txt"
with open(file_path, "r") as file:
    contents = file.read()
    
print("파일 내용:\n", contents)


# 2. 행 단위로 파일 읽기
file_path = "file.txt"
with open(file_path, "r") as file:
    lines = file.readlines()

print("파일 내용:")
for line in lines:
    print(line.strip())

