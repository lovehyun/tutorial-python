# 1. 파일 쓰기
file_path = "file.txt"
data = "Hello, World!"

with open(file_path, "w") as file:
    file.write(data)

print("파일 쓰기 완료")


# 2. 파일에 내용 추가
file_path = "file.txt"
data = "New line"

with open(file_path, "a") as file:
    file.write("\n" + data)

print("파일 내용 추가 완료")
