import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

def get_naver_news(category):
    if category == 'sports':
        url = 'https://sports.news.naver.com/index'
    elif category == 'land':
        url = 'https://land.naver.com/news/'
    else:
        print("Invalid category.")
        return

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    if category == 'sports':
        news = soup.select('.today_list > li')
        print(f"Total {len(news)} sports news found.\n")
        for n in news:
            a_tag = n.select_one('a')
            news_title = a_tag['title']
            news_url = 'https://sports.news.naver.com' + a_tag['href']

            print(news_title)
            print_news_content(news_url)
            print('----------------------------------------')

    elif category == 'land':
        part = input("Select 'headline' or 'trend': ")
        if part not in ['headline', 'trend']:
            print("Invalid part.")
            return

        if part == 'headline':
            news = soup.select('.section_group.NE\=a\:chl > ul > li')
            print(f"Total {len(news)} land headline news found.\n")
            for n in news:
                a_tags = n.select('a')
                print(a_tags[0].text, a_tags[1].text)

        elif part == 'trend':
            news = soup.select('.section_group.NE\=a\:trd > ul > li')
            print(f"Total {len(news)} land trend news found.\n")
            for n in news:
                a_tag = n.select_one('a')
                print(a_tag.text)

def print_news_content(url):
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    news_content = soup.select_one('.news_end')
    if news_content:
        start_span = news_content.find('span')
        end_p = news_content.find('p', class_='source')
        if start_span and end_p:
            content = start_span.next_element
            while content and content != end_p:
                if isinstance(content, str) and content.strip():
                    print(content.strip())
                content = content.next_element
        else:
            print(f'본문 내용을 가져올 수 없습니다. {url}')
    else:
        print(f'본문 내용을 가져올 수 없습니다. {url}')

if __name__ == "__main__":
    category = input("Select 'sports' or 'land': ")
    get_naver_news(category)
