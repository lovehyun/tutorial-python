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

        # print(f"Title: {title}")
        # print(f"URL: {news_content_url}")

        # 해당 뉴스 기사 페이지 내용을 가져오는 함수 호출
        get_news_content(news_content_url)
        break


# 개별 뉴스 기사 페이지의 내용을 가져오는 함수
def get_news_content(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    # 예시: 기사 제목 및 본문 내용 가져오기
    print(soup)
    headline = soup.select_one('h2')
    content = soup.select_one('div#_article_content')

    if headline:
        print(f"Headline: {headline.text.strip()}")
    if content:
        print(f"Content: {content.text.strip()[:200]}...")  # 본문 내용 일부 출력

    print('-' * 80)  # 구분선 출력


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
