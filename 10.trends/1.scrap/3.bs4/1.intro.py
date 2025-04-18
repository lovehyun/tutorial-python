# pip install bs4  (dummy alias)
# pip install beautifulsoup4

from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
    <title>간단한 HTML 예제</title>
</head>
<body>
    <h1>안녕하세요!</h1>
    <p>이것은 간단한 HTML 예제입니다.</p>
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')

# h1 태그의 텍스트 출력
print(soup.h1.text)

# p 태그의 텍스트 출력
print(soup.p.text)
