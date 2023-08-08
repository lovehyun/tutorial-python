from bs4 import BeautifulSoup

html = '''
<html>
<body>
  <div class="content">
    <h1>Title 1</h1>
    <p>Paragraph 1</p>
    <p>Paragraph 2</p>
    <ul>
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </ul>
  </div>
  <div class="content">
    <h1>Title 2</h1>
    <p>Paragraph 3</p>
    <p>Paragraph 4</p>
    <ul>
      <li>Item 4</li>
      <li>Item 5</li>
      <li>Item 6</li>
    </ul>
  </div>
</body>
</html>
'''

soup = BeautifulSoup(html, 'html.parser')

# 클래스가 "content"인 모든 <div> 태그들을 가져오기
content_divs = soup.select('div.content')
for div in content_divs:
    print(div)

# 모든 <p> 태그들을 가져오기
p_tags = soup.select('p')
for p in p_tags:
    print(p)
