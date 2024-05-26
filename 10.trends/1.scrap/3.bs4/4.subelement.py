from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
    <title>간단한 HTML 예제</title>
</head>
<body>
    <div class="container">
        <h1>안녕하세요!</h1>
        <p>이것은 간단한 HTML 예제입니다.</p>
        <ul>
            <li>항목 1</li>
            <li>항목 2</li>
            <li>항목 3</li>
        </ul>
    </div>
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')

# div 태그의 하위 ul 태그 추출
ul_tag = soup.find('div', class_='container').ul

# ul 태그의 모든 li 태그 추출 및 출력
for li in ul_tag.find_all('li'):
    print(li.text)
