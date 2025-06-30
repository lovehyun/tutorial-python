# pip install pyzipper
import os
import pyzipper

directory = '압축할_디렉토리_경로'

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    if os.path.isfile(file_path):
        zip_filename = f"{file_path}.zip"
        
        with pyzipper.AESZipFile(zip_filename, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(b'1234')  # 비밀번호 설정
            zipf.write(file_path, arcname=filename)
            print(f"{filename} → {zip_filename} 압축 완료 (비밀번호: 1234)")

        # 원본 파일 삭제
        os.remove(file_path)
        print(f"원본 파일 {file_path} 삭제 완료")
