# 자연어 처리: 텍스트 데이터를 처리하고 분석하는 기술
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# 텍스트 데이터 전처리
text = "This is a sample sentence."
tokens = word_tokenize(text)
filtered_tokens = [token for token in tokens if token.lower() not in stopwords.words("english")]

print("토큰화 결과:", filtered_tokens)
