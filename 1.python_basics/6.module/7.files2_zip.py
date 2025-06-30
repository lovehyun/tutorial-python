import os
import zipfile

# 압축할 디렉토리 경로
directory = '압축할_디렉토리_경로'

# 디렉토리 내 파일 목록 가져오기
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # 파일인 경우만 처리 (폴더는 제외)
    if os.path.isfile(file_path):
        # zip 파일 이름 만들기 (기존 이름에 .zip 붙임)
        zip_filename = f"{file_path}.zip"
        
        # zip 파일 생성 및 압축
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(file_path, arcname=filename)
            print(f"{filename} → {zip_filename} 압축 완료")

