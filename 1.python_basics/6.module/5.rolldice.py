import random

def roll_dice():
    return random.randint(1, 6)
print("주사위 던지기 결과:", roll_dice())


# 방법1.
# 주사위 n번 던지기
def roll_n_times(times):
    # 0~5 인덱스에 카운트 저장 (1~6 눈금)
    counts = [0, 0, 0, 0, 0, 0]  # counts[0]은 1이 나온 횟수
    for _ in range(times):
        result = roll_dice()
        counts[result - 1] += 1  # 주사위 1 → counts[0], 주사위 6 → counts[5]
    return counts

# 결과 출력
print("주사위 10,000번 던진 통계 (리스트 인덱스 기반):")
counts = roll_n_times(10000)
for i in range(6):
    print(f"{i + 1} 나온 횟수: {counts[i]}회, 비율: {counts[i] / sum(counts):.2%}")


# 방법2. 모던 python 스타일
# 결과를 저장할 딕셔너리 초기화
dice_counts = {i: 0 for i in range(1, 7)}
# {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

# 주사위를 n번(10,000번) 던지기
def roll_dices(numbers):
    for _ in range(numbers):
        result = roll_dice()
        dice_counts[result] += 1

# 결과 출력
print("주사위 10,000번 던진 통계:")

trial = 10_000
roll_dices(trial)

for dice_num, count in dice_counts.items():
# for dice_num, count in sorted(dice_counts.items()):
    print(f"{dice_num} 나온 횟수: {count}회, 비율: {count / trial:.2%}")
