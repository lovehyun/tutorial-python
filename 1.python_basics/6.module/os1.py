import os

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

