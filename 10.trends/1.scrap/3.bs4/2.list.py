from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
    <title>간단한 HTML 예제</title>
</head>
<body>
    <h1>안녕하세요!</h1>
    <p>이것은 간단한 HTML 예제입니다.</p>
    <ul>
        <li>항목 1</li>
        <li>항목 2</li>
        <li>항목 3</li>
    </ul>
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')

# ul 태그의 모든 li 태그 추출 및 출력
for li in soup.ul.find_all('li'):
    print(li.text)
