import requests

# 키연동방식
# https://api.exchangeratesapi.io/latest?base=USD

# 네이버 API 활용
base_url = 'https://m.search.naver.com/p/csearch/content/qapirender.nhn?key=calculator&pkid=141&q=환율&where=m'
usd_url = base_url + '&u1=keb&u6=standardUnit&u7=0&u3=USD&u4=KRW&u8=down&u2=1'
jpy_url = base_url + '&u1=keb&u6=standardUnit&u7=0&u3=JPY&u4=KRW&u8=down&u2=100'

response = requests.get(jpy_url)
data = response.json()
print(data)
print(data['country'][1]['value'])
