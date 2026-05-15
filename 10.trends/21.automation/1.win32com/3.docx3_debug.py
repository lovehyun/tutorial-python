import win32com.client
import os
import sys

def complete_debug():
    print("=== Word COM 자동화 디버깅 ===")
    print(f"Python 버전: {sys.version}")
    print(f"운영체제: {os.name}")
    
    try:
        print("\n1. Word 애플리케이션 생성 중...")
        word = win32com.client.Dispatch("Word.Application")
        print("   ✓ Word 애플리케이션 생성 성공")
        
        print("\n2. Word 창 표시 설정 중...")
        word.Visible = True
        print("   ✓ Visible = True 설정 완료")
        
        print("\n3. 새 문서 생성 중...")
        doc = word.Documents.Add()
        print("   ✓ 새 문서 생성 성공")
        
        print("\n4. 텍스트 입력 중...")
        doc.Content.Text = "테스트: 1주차 내용입니다."
        print("   ✓ 텍스트 입력 완료")
        
        print("\n*** Word 창이 보이나요? ***")
        input("확인했으면 Enter를 누르세요...")
        
        # 저장
        doc.Save()
        print("   ✓ 문서 저장 완료")
        
        # 문서 닫기
        doc.Close()
        print("   ✓ 문서 닫기 완료")
        
        word.Quit()
        print("   ✓ Word 종료 완료")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

complete_debug()
