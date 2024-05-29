import requests
from bs4 import BeautifulSoup

# 웹 페이지에 GET 요청 보내기
url = 'http://www.cine21.com/rank/boxoffice/domestic'
response = requests.get(url)

# 응답의 텍스트를 BeautifulSoup으로 파싱
bs = BeautifulSoup(response.text, 'html.parser')

# boxoffice_list_content ID를 가진 div 찾기
boxoffice_list_content = bs.find('div', id='boxoffice_list_content')
print(boxoffice_list_content)


# boxoffice_list_content 내의 모든 boxoffice_li 클래스를 가진 li 요소들 찾기
boxoffice_li_list = boxoffice_list_content.find_all('li', class_='boxoffice_li')
print(boxoffice_li_list)

# 각 boxoffice_li에 대해 mov_name, people_num 클래스를 가진 div의 텍스트 출력
# for boxoffice_li in boxoffice_li_list:
#     mov_name_div = boxoffice_li.find('div', class_='mov_name')
#     people_num_div = boxoffice_li.find('div', class_='people_num')
#     mov_name = mov_name_div.get_text(strip=True) if mov_name_div else ''
#     people_num = people_num_div.get_text(strip=True) if people_num_div else ''
#     print(f"영화 제목: {mov_name}, 관객 수: {people_num}")
