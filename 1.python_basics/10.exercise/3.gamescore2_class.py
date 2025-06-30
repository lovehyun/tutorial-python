class Game:
    def __init__(self):
        # 게임 상태 저장
        self.history = []
        self.high_score = 0

    def input_score(self):
        try:
            score = int(input("점수: "))
        except ValueError:
            print('숫자를 입력해주세요.')
            return

        name = input("이름: ")
        self.store_result(score, name)

    def store_result(self, score, name):
        self.history.append((score, name))
        if score > self.high_score:
            self.high_score = score

    def check_highscore(self):
        print('최고점수: ', self.high_score)

    def show_history(self):
        print('============')
        print('점수, 이름')
        print('============')
        for score, name in self.history:
            print(f"{score:3d}, {name:>5}")

    def input_mode(self):
        mode_ops = ['high', 'history', 'score', 'quit']
        mode = input("원하는 모드를 입력하시오: ")

        if mode not in mode_ops:
            print("유효하지 않은 모드입니다. 다시 입력해주세요.")
            return

        if mode == 'score':
            self.input_score()

        elif mode == 'high':
            self.check_highscore()

        elif mode == 'history':
            self.show_history()

        elif mode == 'quit':
            print("게임을 종료합니다.")
            exit(0)

    def run(self):
        while True:
            self.input_mode()

# 실행 부분
if __name__ == "__main__":
    game = Game()
    game.run()
