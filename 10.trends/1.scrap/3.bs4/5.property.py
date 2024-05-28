from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
    <title>간단한 HTML 예제</title>
</head>
<body>
    <a href="https://www.example.com">예제 링크</a>
    <img src="example.jpg" alt="예제 이미지">
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')

# 링크 태그의 href 속성 값 출력
link_tag = soup.a
print(link_tag['href'])

# 이미지 태그의 src 속성 값 출력
img_tag = soup.img
print(img_tag['src'])


# 스크린샷 저장하기
soup.save_screenshot('example_com.png')

soup.quit()
