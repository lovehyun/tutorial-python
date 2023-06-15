try:
    with open("file.txt", "r") as file:
        contents = file.read()
    print("파일 내용:\n", contents)
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except IOError:
    print("파일을 읽을 수 없습니다.")
