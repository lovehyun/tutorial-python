# 1. 텍스트 파일 쓰기
with open('example.txt', 'w') as file:
    file.write("Hello, world!\n")
    file.write("This is a test file.\n")
    file.write("Writing to a text file in Python is easy.\n")

print("텍스트 파일에 데이터를 썼습니다.")


# 2. 텍스트 파일 읽기
with open('example.txt', 'r') as file:
    content = file.read()

print("파일 내용:")
print(content)

# 3. 텍스트 파일을 줄 단위로 읽기
with open('example.txt', 'r') as file:
    for line in file:
        print(line, end='')

# 혹은
with open('example.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line, end='')


# 4. 텍스트 파일에 추가
with open('example.txt', 'a') as file:
    file.write("Appending a new line to the file.\n")

print("텍스트 파일에 데이터를 추가했습니다.")
