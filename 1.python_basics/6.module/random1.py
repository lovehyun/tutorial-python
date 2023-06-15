# Random 모듈 활용
import random

# 1부터 6까지의 난수 생성 (주사위 던지기)
dice_roll = random.randint(1, 6)
print("주사위 던지기 결과:", dice_roll)

# 리스트 요소 무작위로 섞기
my_list = [1, 2, 3, 4, 5]
random.shuffle(my_list)
print("섞인 리스트:", my_list)

