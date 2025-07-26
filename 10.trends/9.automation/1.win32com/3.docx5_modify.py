import win32com.client
import os

def find_and_replace_word(file_path, find_text, replace_text):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    doc = word.Documents.Open(os.path.abspath(file_path))
    
    # 찾기/바꾸기 실행
    find_replace = doc.Content.Find
    find_replace.Text = find_text
    find_replace.Replacement.Text = replace_text
    find_replace.Execute(Replace=2)  # wdReplaceAll
    
    doc.Save()
    doc.Close()
    word.Quit()

def find_and_replace_word2(file_path, find_text, replace_text):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = True  # 디버깅을 위해 True로 설정
    
    doc = word.Documents.Open(os.path.abspath(file_path))
    
    # Selection 객체 사용 (가장 확실한 방법)
    selection = word.Selection
    selection.HomeKey(6)  # 문서 처음으로 이동
    
    # 찾기/바꾸기 설정
    find = selection.Find
    find.ClearFormatting()
    find.Replacement.ClearFormatting()
    
    find.Text = find_text
    find.Replacement.Text = replace_text
    find.Forward = True
    find.Wrap = 1  # wdFindContinue
    find.Format = False
    find.MatchCase = False
    find.MatchWholeWord = False
    
    # 모든 항목 바꾸기
    find.Execute(Replace=2)  # wdReplaceAll
    
    doc.Save()
    doc.Close()
    word.Quit()
    
def modify_word_table():
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = True
    
    doc = word.Documents.Open(os.path.abspath("docs/test.docx"))
    
    # 첫 번째 표 가져오기
    if doc.Tables.Count > 0:
        table = doc.Tables(1)  # 첫 번째 표
        
        # 표의 모든 셀 검사
        for row in range(1, table.Rows.Count + 1):
            for col in range(1, table.Columns.Count + 1):
                try:
                    cell = table.Cell(row, col)
                    cell_text = cell.Range.Text.strip()
                    
                    # "1주차"를 "2주차"로 변경
                    if "1주차" in cell_text:
                        new_text = cell_text.replace("1주차", "2주차")
                        cell.Range.Text = new_text
                        
                except:
                    continue  # 병합된 셀 등 예외 처리
    
    doc.Save()
    doc.Close()
    word.Quit()

def advanced_word_operations():
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = True
    
    doc = word.Documents.Open(os.path.abspath("docs/test.docx"))
    
    # Selection 객체 사용
    selection = word.Selection
    
    # 특정 텍스트 찾기
    selection.Find.ClearFormatting()
    selection.Find.Text = "중요한 내용"
    
    if selection.Find.Execute():
        # 찾은 텍스트를 굵게 만들기
        selection.Font.Bold = True
        selection.Font.Color = 255  # 빨간색
    
    # 문서 전체에서 특정 스타일 적용
    for paragraph in doc.Paragraphs:
        if "제목" in paragraph.Range.Text:
            paragraph.Range.Font.Size = 16
            paragraph.Range.Font.Bold = True
    
    doc.Save()
    doc.Close()
    word.Quit()

# 사용 예시
# find_and_replace_word("docs/test.docx", "1주차", "2주차")
find_and_replace_word2("docs/test.docx", "1주차", "2주차")
