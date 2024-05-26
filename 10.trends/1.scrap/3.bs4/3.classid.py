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
    </div>
    <div id="footer">
        <p>저작권 © 2024. 모든 권리 보유됨.</p>
    </div>
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')

# 클래스가 "container"인 div 태그의 내용 출력
container_div = soup.find('div', class_='container')
print(container_div.h1.text)
print(container_div.p.text)

# id가 "footer"인 div 태그의 내용 출력
footer_div = soup.find('div', id='footer')
print(footer_div.p.text)
