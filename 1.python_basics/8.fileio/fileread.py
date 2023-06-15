# 파일 읽기
file_path = "file.txt"
with open(file_path, "r") as file:
    contents = file.read()
print("파일 내용:\n", contents)
