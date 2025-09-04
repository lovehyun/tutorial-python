# -*- coding: utf-8 -*-
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# 긴 텍스트 예시
text = """
파이썬은 인공지능, 데이터 분석, 웹 개발, 보안, 자동화 등 다양한 분야에서 사용됩니다.
워드클라우드를 활용하면 중요한 키워드를 시각적으로 강조할 수 있습니다.
특히 교육, 논문, 리포트 작성 시 많이 쓰입니다.
하트 모양, 사과 모양, 자전거 모양 등 원하는 마스크 이미지를 적용하여 
시각적으로 더 재미있는 표현을 할 수 있습니다.
"""

# 하트 모양 마스크 불러오기 (흑백 PNG 파일 준비 필요)
# mask = np.array(Image.open("heart.png"))  # 예: 흰 배경에 검정 하트 모양 PNG
mask = np.array(Image.open("apple.png"))  # 예: 흰 배경에 검정 사과 모양 PNG

# 워드클라우드 생성
wc = WordCloud(
    font_path="malgun.ttf",   # 한글 폰트 지정
    mask=mask,                # 마스크 적용
    background_color="white",
    contour_color="red",      # 외곽선 색
    contour_width=2,
    width=800,
    height=800
).generate(text)

# 출력
plt.figure(figsize=(8, 8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
