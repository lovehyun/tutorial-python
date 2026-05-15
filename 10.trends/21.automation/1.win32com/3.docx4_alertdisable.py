import win32com.client
import os

def word_automation_no_prompts():
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        # 중요: 모든 알림/확인 대화상자 비활성화
        word.DisplayAlerts = False
        word.ScreenUpdating = False
        
        # 파일 열기
        file_path = os.path.abspath("docs/test.docx")
        doc = word.Documents.Open(file_path)
        
        # 작업 수행
        content = doc.Range()
        find = content.Find
        find.Execute(
            FindText="1주차",
            ReplaceWith="2주차",
            Replace=2
        )
        
        # 강제 저장 (확인 없이)
        doc.Save()
        print("저장 완료")
        
        # 강제 닫기 (확인 없이)
        doc.Close(SaveChanges=False)  # 이미 저장했으므로 False
        
    except Exception as e:
        print(f"오류: {e}")
    
    finally:
        if word:
            word.DisplayAlerts = True  # 원래대로 복구
            word.Quit()
            print("Word 종료")

word_automation_no_prompts()
