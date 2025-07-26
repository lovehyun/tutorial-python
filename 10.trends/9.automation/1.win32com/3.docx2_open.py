import win32com.client
import os

def test_word_file_open():
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = True
        
        # 파일 경로 확인
        file_path = os.path.abspath("docs/test.docx")
        print(f"파일 경로: {file_path}")
        print(f"파일 존재: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            print("파일이 없으므로 새 문서 생성")
            doc = word.Documents.Add()
            doc.Content.Text = "테스트 문서입니다. 1주차 내용을 포함합니다."
            doc.SaveAs(file_path)
        else:
            print("기존 파일 열기")
            doc = word.Documents.Open(file_path)
        
        print("파일 열기 성공!")
        input("계속하려면 Enter...")
        
        word.Quit()
        
    except Exception as e:
        print(f"상세 오류: {e}")
        import traceback
        traceback.print_exc()

test_word_file_open()
