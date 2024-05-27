import requests
from bs4 import BeautifulSoup


def get_naver_sportsnews():
    data = requests.get('https://sports.news.naver.com/index')
    soup = BeautifulSoup(data.text, 'html.parser')

    # print(soup)
    news = soup.select('.today_list > li')
    print(len(news))

    for n in news:
        # 미션1. 타이틀 제목을 가져온다.
        a_tag = n.select_one('a')
        print(a_tag['title']) # a 태그의 title 로 가져온다

        title = n.select_one('.title') # 클래스 title 로 가져온다
        # print(title.text)

        strong = n.select_one('strong') # 태그명 strong 으로 가져온다
        # print(strong.text)

        news_content_url = a_tag['href']
        print(news_content_url)


# 동적으로 삽입되는 뉴스기사라 requests 로 가져올 수 없음.
def get_naver_sportsnews_recommend():
    data = requests.get('https://sports.news.naver.com/index')
    soup = BeautifulSoup(data.text, 'html.parser')

    news = soup.select('#_sports_home_airs_area')
    print(len(news))
    print(news)


if __name__ == "__main__":
    get_naver_sportsnews()
    # get_naver_sportsnews_recommend()
