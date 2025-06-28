# 이미지 처리:
from PIL import Image, ImageFilter

# 이미지 열기
image = Image.open("data/cats.jpg")

# 이미지 크기 조정
resized_image = image.resize((400, 300))

# 이미지 필터 적용
filtered_image = image.filter(ImageFilter.BLUR)

# 이미지 저장
resized_image.save("resized_image.jpg")
filtered_image.save("filtered_image.jpg")
