# 다른 예외를 가로채고 다시 발생시키기

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"{file_path} 파일을 찾을 수 없습니다.") from e

try:
    content = read_file("nonexistent_file.txt")
except FileNotFoundError as e:
    print(e)

