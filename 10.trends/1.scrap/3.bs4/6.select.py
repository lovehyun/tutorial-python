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
    <div class="content" id="main-content">
        <p>여기에는 <b>강조된 텍스트</b>와 <i>기울임 텍스트</i>가 있습니다.</p>
        <p>추가 텍스트 <a href="https://www.yetanotherexample.com" title="Yet Another Site">또 다른 링크</a></p>
    </div>
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')

# 1. select_one 사용 예제
# 첫 번째 <a> 태그의 href 속성 값 출력
link_tag = soup.select_one('a')
print("First link tag href:", link_tag['href'])

# 첫 번째 <img> 태그의 src 속성 값 출력
first_img_tag = soup.select_one('img')
print("First image tag src:", first_img_tag['src'])


# 2. select 사용 예제
# 모든 <a> 태그의 href 속성 값 출력
print("\nAll link tags href:")
all_link_tags = soup.select('a')
for tag in all_link_tags:
    print(tag['href'])

# 모든 <img> 태그의 src 속성 값 출력
print("\nAll image tags src:")
all_img_tags = soup.select('img')
for tag in all_img_tags:
    print(tag['src'])


# 3. 특정 클래스나 아이디로 태그 선택
# 클래스가 'content'인 div 태그 선택
content_div = soup.select_one('div.content')
print("\nDiv with class 'content':", content_div)

# 아이디가 'main-content'인 div 태그 선택
main_content_div = soup.select_one('#main-content')
print("\nDiv with id 'main-content':", main_content_div)


# 4. 특정 태그 내의 특정 태그 선택
# 클래스가 'content'인 div 태그 내의 모든 <p> 태그 선택
print("\nAll <p> tags inside div with class 'content':")
p_tags_in_content_div = soup.select('div.content p')
for tag in p_tags_in_content_div:
    print(tag.get_text())

# 첫 번째 <p> 태그 내의 <b> 태그 선택
first_p_tag = soup.select_one('p')
b_tag_in_first_p = first_p_tag.select_one('b')
print("\nBold text in first paragraph:", b_tag_in_first_p.get_text())

# 첫 번째 <p> 태그 내의 <i> 태그 선택
i_tag_in_first_p = first_p_tag.select_one('i')
print("Italic text in first paragraph:", i_tag_in_first_p.get_text())
