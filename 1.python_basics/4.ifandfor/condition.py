# 1. 성적 등급 매기기
score = 85
if score >= 90:
    print("A grade")
elif score >= 80:
    print("B grade")
elif score >= 70:
    print("C grade")
elif score >= 60:
    print("D grade")
else:
    print("F grade")


# 2. 사용자 입력 검증하기
password = input("Enter your password: ")
if len(password) >= 8:
    print("Valid password")
else:
    print("Invalid password")


# 3. 파일 유형 확인하기 (확장자 기준)
filename = "example.txt"
if filename.endswith(".txt"):
    print("Text file")
elif filename.endswith(".jpg") or filename.endswith(".png"):
    print("Image file")
else:
    print("Unknown file type")


