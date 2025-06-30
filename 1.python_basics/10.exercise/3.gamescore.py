history = []
high_score = 0

def input_score():
    score = int(input("점수: "))
    name = input("이름: ")

    return score, name

def store_result(score, name):    
    game_score = (score, name)
    history.append(game_score)

def check_highscore():
    global high_score
    for score, _ in history:
        if score > high_score:
            high_score = score

def input_mode():
    mode_ops = ['high', 'history', 'score', 'quit']
    mode = input("원하는 모드를 입력하시오: ")

    if (mode not in mode_ops):
        mode = input("원하는 모드를 입력하시오: ")

    if mode == 'score':
        score, name = input_score()
        store_result(score, name)

    if mode == 'high':
        check_highscore()
        print('최고점수: ', high_score)

    if mode == 'history': # 히스토리 점수 기록
        print('============')
        print('점수, 이름')
        print('============')
        for score, name in history:
            print(f"{score:3d}, {name:>5}") # 숫자 3d, 스트링 5, 오른쪽/왼쪽 정렬 ><
    
    if mode == 'quit':
        exit(1)
    
    return mode

if __name__ == "__main__":
    while True:
        input_mode()
