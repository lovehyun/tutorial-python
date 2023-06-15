# 이미지 처리:
from PIL import Image

# 이미지 열기
image = Image.open("image.jpg")

# 이미지 크기 조정
resized_image = image.resize((800, 600))

# 이미지 필터 적용
filtered_image = image.filter(ImageFilter.BLUR)

# 이미지 저장
resized_image.save("resized_image.jpg")
filtered_image.save("filtered_image.jpg")
