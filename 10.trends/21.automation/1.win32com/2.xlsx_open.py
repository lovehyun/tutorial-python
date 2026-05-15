# pip install pywin32

import win32com.client
import os

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True

# 현재 디렉토리 기준으로 절대 경로 생성
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "docs", "test.xlsx")
print(f"파일 경로: {file_path}")

# 파일 존재 확인
if os.path.exists(file_path):
    workbook = excel.Workbooks.Open(file_path)
else:
    print(f"파일이 존재하지 않습니다: {file_path}")
