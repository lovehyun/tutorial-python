import win32com.client
import os

def modify_excel():
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    
    # 파일 열기
    workbook = excel.Workbooks.Open(os.path.abspath("docs/test.xlsx"))
    worksheet = workbook.ActiveSheet
    
    # 셀 값 읽기
    cell_value = worksheet.Cells(1, 1).Value  # A1 셀
    print(f"A1 셀 값: {cell_value}")
    
    # 셀 값 변경
    worksheet.Cells(1, 1).Value = "새로운 값"
    worksheet.Cells(2, 2).Value = "B2에 '1주차' 입력"
    
    # 저장 및 종료
    workbook.Save()
    workbook.Close()
    excel.Quit()

def find_and_replace_excel(file_path, find_text, replace_text):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  # 백그라운드 실행
    
    workbook = excel.Workbooks.Open(os.path.abspath(file_path))
    
    # 모든 워크시트에서 찾기/바꾸기
    for worksheet in workbook.Worksheets:
        # 전체 범위에서 찾기/바꾸기 실행
        worksheet.Cells.Replace(
            What=find_text,        # 찾을 텍스트
            Replacement=replace_text,  # 바꿀 텍스트
            LookAt=2,             # xlPart (부분 일치)
            SearchOrder=1,        # xlByRows
            MatchCase=False       # 대소문자 구분 안함
        )
    
    workbook.Save()
    workbook.Close()
    excel.Quit()

def modify_table_excel():
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    
    workbook = excel.Workbooks.Open(os.path.abspath("docs/test.xlsx"))
    worksheet = workbook.ActiveSheet
    
    # 특정 범위의 데이터 읽기
    data_range = worksheet.Range("A1:C10")
    values = data_range.Value
    
    # 데이터 수정
    for i, row in enumerate(values):
        if row and "1주차" in str(row[0]):  # 첫 번째 열에 "1주차"가 있으면
            worksheet.Cells(i+1, 1).Value = str(row[0]).replace("1주차", "2주차")
    
    workbook.Save()
    workbook.Close()
    excel.Quit()
    
# 사용 예시
modify_excel()
modify_table_excel()
find_and_replace_excel("docs/test.xlsx", "2주차", "3주차")
