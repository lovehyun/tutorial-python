from bs4 import BeautifulSoup

# HTML 파일을 읽어서 파일 객체로 열기
with open('example.html', 'r') as file:
    html_content = file.read()

# BeautifulSoup를 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# 파싱된 HTML에서 원하는 요소 추출
# 예시로 div 태그 안의 h1 태그와 p 태그의 텍스트를 가져옵니다.
div_tag = soup.find('div', class_='content')
if div_tag:
    h1_tag = div_tag.find('h1')
    p_tag = div_tag.find('p')

    if h1_tag and p_tag:
        print("제목:", h1_tag.get_text())
        print("내용:", p_tag.get_text())
    else:
        print("제목 또는 내용이 존재하지 않습니다.")
else:
    print("div 태그가 존재하지 않습니다.")
