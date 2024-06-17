import requests
from bs4 import BeautifulSoup

data = requests.get('https://www.pythonscraping.com/pages/page3.html')

# print(data)
# print(data.text)

soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)

gifts = soup.select('#giftList > tr')
# giftList = soup.find('table', id='giftList')
# gifts = giftList.find_all('tr')

# print(gifts)
print(len(gifts))

my_gifts = gifts[1:]
print(len(my_gifts))

for g in my_gifts:
    # print(g)
    tds = g.select('td')
    # print(len(tds))
    
    print(f"TITLE:{tds[0].text.strip()}, PRICE:{tds[2].text.strip()}")
    # print(f"PIC:{tds[3].img['src']}")
