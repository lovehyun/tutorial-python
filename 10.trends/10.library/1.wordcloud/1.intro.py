# pip install wordcloud matplotlib
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 샘플 텍스트
text = """
파이썬은 데이터 분석, 인공지능, 웹 개발 등 다양한 분야에서 활용되는 언어입니다.
워드클라우드를 이용하면 텍스트에서 자주 등장하는 단어를 시각적으로 표현할 수 있습니다.
"""

# 워드클라우드 생성
wc = WordCloud(
    font_path="malgun.ttf",  # Windows: "malgun.ttf", Mac: "AppleGothic", Linux: 나눔고딕 등
    width=800,
    height=400,
    background_color="white"
).generate(text)

# 결과 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
