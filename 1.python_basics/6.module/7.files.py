import os

# 탐색할 디렉토리 경로
directory = '탐색할_디렉토리_경로'

# 디렉토리 안의 모든 파일 출력
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        print(filename)
