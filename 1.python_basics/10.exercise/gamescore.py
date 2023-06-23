history = []
high_score = 0

def input_score():
    score = int(input("점수: "))
    name = input("이름: ")

    return score, name

def store_result(score, name):    
    game_score = (score, name)
    history.append(game_score)

def print_highscore():
    high = 0
    for score, _ in history:
        print(score)

def input_mode():
    mode_ops = ['high', 'history', 'score']
    mode = input("원하는 모드를 입력하시오: ")
    if (mode not in mode_ops):
        mode = input("원하는 모드를 입력하시오: ")

    if mode == 'high':
        print('최고점수: ', high_score)
        print_highscore()
    if mode == 'history':
        print('==========')
        print('점수, 이름')
        print('==========')
        print(history)
    if mode == 'quit':
        exit(1)
    
    return mode

if __name__ == "__main__":
    while True:
        op = input_mode()
        if op == 'score':
            score, name = input_score()
            store_result(score, name)
