# 파일 쓰기
file_path = "file.txt"
data = "Hello, World!"
with open(file_path, "w") as file:
    file.write(data)
print("파일 쓰기 완료")
