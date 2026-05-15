import win32com.client

try:
    # Word 애플리케이션 생성 테스트
    word = win32com.client.Dispatch("Word.Application")
    print("Word 애플리케이션 생성 성공")
    
    # 창 표시 설정
    word.Visible = True
    print("Word 창 표시 설정")
    
    # 새 문서 생성 테스트
    doc = word.Documents.Add()
    print("새 문서 생성 성공")
    
    # 잠시 대기
    input("Enter를 눌러서 Word를 종료하세요...")
    
    word.Quit()
    
except Exception as e:
    print(f"오류 발생: {e}")
    print("Word가 설치되어 있는지 확인하세요")
