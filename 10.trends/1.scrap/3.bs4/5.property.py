from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
    <title>간단한 HTML 예제</title>
</head>
<body>
    <a href="https://www.example.com">예제 링크</a>
    <img src="example.jpg" alt="예제 이미지">
    <img src="example2.jpg" alt="예제 이미지2" width="500" height="600">
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

# 두 번째 이미지 태그 가져오기
img_tags = soup.find_all('img')
img_tag2 = img_tags[1] if len(img_tags) > 1 else None

print(f"Src: {img_tag['src']}, Alt: {img_tag.get('alt', 'No alt')}, Width: {img_tag.get('width', 'No width')}, Height: {img_tag.get('height', 'No height')}")
print(f"Src: {img_tag2['src']}, Alt: {img_tag2.get('alt', 'No alt')}, Width: {img_tag2.get('width', 'No width')}, Height: {img_tag2.get('height', 'No height')}")
