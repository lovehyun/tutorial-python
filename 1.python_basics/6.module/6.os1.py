# https://docs.python.org/ko/3/library/os.html
import os

# 모듈명.함수명

# 1. 작업 디렉토리 확인
current_dir = os.getcwd()
print("현재 작업 디렉토리:", current_dir)


# 2. 새 디렉토리 생성
new_dir = "new_directory"
os.mkdir(new_dir)
print("디렉토리 생성 완료:", new_dir)


# 3. 새 디렉토리 삭제
os.rmdir(new_dir)
print("디렉토리 삭제 완료: ", new_dir)


# 4. 환경 변수 접근
python_path = os.getenv("PYTHONPATH")
print("PYTHONPATH 환경 변수 값:", python_path)


# 5. 시스템 명령 실행
command = "dir"
# command = "ls -l"
os.system(command)


# 6. 디렉토리 변경
os.chdir('C:/src/SESAC_PY')
# os.chdir('/path/to/directory')
print(f"현재 작업 디렉토리: {os.getcwd()}")


# 7. 파일 존재 여부 확인
file_exists = os.path.exists('some_file.txt')
print(f"'some_file.txt' 존재 여부: {file_exists}")
