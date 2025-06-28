# 자연어 처리: 텍스트 데이터를 처리하고 분석하는 기술
# pip install nltk==3.7

import nltk
nltk.download('punkt')   # 토큰화용 데이터 (period, dot, ...)
nltk.download('stopwords')   # 불용어 데이터 (관사(a), 전치사(in), 접속사(and), ...)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# 텍스트 데이터 전처리
text = "This is a sample sentence."
tokens = word_tokenize(text)
filtered_tokens = [token for token in tokens if token.lower() not in stopwords.words("english")]

print("토큰화 결과:", filtered_tokens)

# 더 긴 텍스트 데이터
text = "In today's fast-paced world, artificial intelligence plays a crucial role in automating tasks, improving efficiency, and providing innovative solutions across various industries."

tokens = word_tokenize(text)
filtered_tokens = [token for token in tokens if token.lower() not in stopwords.words("english")]

print("토큰화 결과:", filtered_tokens)
