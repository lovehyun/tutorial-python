# pip install pywin32

import win32com.client

# Excel 자동화
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
workbook = excel.Workbooks.Open("파일경로.xlsx")

# Word 자동화  
word = win32com.client.Dispatch("Word.Application")
word.Visible = True
doc = word.Documents.Open("파일경로.docx")

# 아래한글 자동화
hwp = win32com.client.Dispatch("HWPFrame.HwpObject")
hwp.Open("파일경로.hwpx")
