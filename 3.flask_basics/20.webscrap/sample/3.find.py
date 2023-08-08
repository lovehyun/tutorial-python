from bs4 import BeautifulSoup

html = '''
<html>
<body>
  <div class="content">
    <h1>Title</h1>
    <p>Paragraph 1</p>
    <p>Paragraph 2</p>
    <ul>
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </ul>
  </div>
  <div class="sidebar">
    <h2>Sidebar Title</h2>
    <p>Sidebar content</p>
  </div>
</body>
</html>
'''

soup = BeautifulSoup(html, 'html.parser')

# 클래스가 "sidebar"인 <div> 태그의 모든 <p> 태그들 가져오기
sidebar_div = soup.find('div', class_='sidebar')
p_tags_in_sidebar = sidebar_div.find_all('p')
for p_tag in p_tags_in_sidebar:
    print(p_tag.get_text())
