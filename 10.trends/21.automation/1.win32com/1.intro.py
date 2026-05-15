try:
    import win32com.client
    print("win32com 모듈 로드 성공")
except ImportError:
    print("win32com 모듈이 설치되지 않았습니다.")
    print("pip install pywin32 를 실행하세요")
