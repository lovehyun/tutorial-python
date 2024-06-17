import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.pythonscraping.com/pages/page3.html', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)  # HTML을 받아온 것을 확인할 수 있다.


# select를 이용해서, tr들을 불러오기
gifts = soup.select('#giftList > tr')
print(len(gifts)) # 6

my_gifts = gifts[1:] # 타이틀 빼고 본문
print(len(my_gifts)) # 5개 항목
# print(my_gifts)

for g in my_gifts:
    tds = g.select('td')
    print(len(tds)) # 4개 항목
    # print(tds[0].text.strip(), tds[2].text.strip())
    # print(tds[3].img['src'])
