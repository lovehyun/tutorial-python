import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

def get_naver_news():
    data = requests.get('https://sports.news.naver.com/index', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # print(soup)  # HTML을 받아온 것을 확인할 수 있다.

    news = soup.select('.today_list > li')
    print(len(news)) # 6

    for n in news:
        a_tag = n.select_one('a') # 태그로 가져온다
        print(a_tag['title'])

        title = n.select_one('.title') # 클래스로 가져온다
        print(title.text)


def get_naver_land(part):
    data = requests.get('https://land.naver.com/news/',headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # print(soup)  # HTML을 받아온 것을 확인할 수 있다.

    if part == 'headline': 
        # content > div > div > div.section_group.NE\=a\:chl > ul
        # news = soup.select('.section_group.NE\=a\:chl > ul > li')
        content = soup.select_one('#container > #content')
        section_group = content.select_one('.section_group')
        news = section_group.select('.list_type > li')
        print(len(news)) # 7

        for n in news:
            a_tags = n.select('a')
            print(len(a_tags))
            print(a_tags[0].text, a_tags[1].text)

    if part == 'trend':
        # news = soup.select('.section_group.NE\=a\:trd > ul > li')
        content = soup.select_one('#container > #content')
        section_group = content.select('.section_group')[3]
        news = section_group.select('.list_type > li')
        print(len(section_group))
        print(len(news)) # 7

        for n in news:
            a_tag = n.select_one('a')
            # print(len(a_tag))
            print(a_tag.text)


if __name__ == "__main__":
    # get_naver_news()
    # get_naver_land('headline')
    get_naver_land('trend')
