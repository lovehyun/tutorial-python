import random
import time
import os
import sys

# Windows에서 방향키 입력을 위한 모듈
try:
    import msvcrt
    WINDOWS = True
except ImportError:
    import termios
    import tty
    WINDOWS = False

class SnakeGame:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.snake = [(width//2, height//2)]  # 뱀의 몸통 (x, y 좌표들)
        self.direction = (1, 0)  # 오른쪽으로 시작
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
        # 게임판 경계
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
    
    def generate_food(self):
        """
        뱀이 없는 위치에 랜덤하게 먹이 생성
        """
        while True:
            food = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        """
        뱀을 현재 방향으로 한 칸 이동
        """
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # 벽에 충돌 검사
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return
        
        # 자기 몸통에 충돌 검사
        if new_head in self.snake:
            self.game_over = True
            return
        
        # 새로운 머리 추가
        self.snake.insert(0, new_head)
        
        # 먹이를 먹었는지 확인
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # 먹이를 안 먹었으면 꼬리 제거 (길이 유지)
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """
        방향 변경 (반대 방향으로는 갈 수 없음)
        """
        dx, dy = self.direction
        new_dx, new_dy = new_direction
        
        # 반대 방향인지 확인
        if (dx, dy) != (-new_dx, -new_dy):
            self.direction = new_direction
    
    def display(self):
        """
        게임 화면 출력
        """
        # 화면 지우기
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 게임판 초기화
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # 뱀 그리기
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                board[y][x] = '●'  # 머리
            else:
                board[y][x] = '○'  # 몸통
        
        # 먹이 그리기
        food_x, food_y = self.food
        board[food_y][food_x] = '🍎'
        
        # 상단 경계
        print('┌' + '─' * (self.width * 2) + '┐')
        
        # 게임판 출력
        for row in board:
            print('│', end='')
            for cell in row:
                print(cell + ' ', end='')
            print('│')
        
        # 하단 경계
        print('└' + '─' * (self.width * 2) + '┘')
        
        # 점수 및 조작법 출력
        print(f"점수: {self.score}")
        print("조작: W(위) A(왼쪽) S(아래) D(오른쪽) Q(종료)")
    
    def get_input(self):
        """
        키보드 입력 받기 (논블로킹)
        """
        if WINDOWS:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                return key
        else:
            # Linux/Mac용 (간단 버전)
            # 실제로는 더 복잡한 구현이 필요합니다
            return None
        return None

def simple_snake_game():
    """
    간단한 버전의 뱀 게임 (입력 후 이동)
    """
    print("🐍 콘솔 뱀 게임 🐍")
    print("W(위), A(왼쪽), S(아래), D(오른쪽)으로 이동")
    print("Q를 입력하면 게임 종료")
    print("엔터를 누르면 한 칸씩 이동합니다")
    print("-" * 40)
    
    game = SnakeGame(15, 8)
    
    while not game.game_over:
        game.display()
        
        # 사용자 입력
        user_input = input("방향 입력 (W/A/S/D) 또는 엔터로 계속: ").lower()
        
        if user_input == 'q':
            break
        elif user_input == 'w':
            game.change_direction((0, -1))  # 위
        elif user_input == 'a':
            game.change_direction((-1, 0))  # 왼쪽
        elif user_input == 's':
            game.change_direction((0, 1))   # 아래
        elif user_input == 'd':
            game.change_direction((1, 0))   # 오른쪽
        
        # 뱀 이동
        game.move_snake()
    
    # 게임 오버
    game.display()
    if game.game_over:
        print("💀 게임 오버! 💀")
    print(f"최종 점수: {game.score}")

def auto_snake_demo():
    """
    자동으로 움직이는 뱀 게임 데모
    """
    print("🤖 자동 뱀 게임 데모 🤖")
    print("뱀이 자동으로 움직입니다!")
    print("아무 키나 누르면 종료됩니다")
    print("-" * 40)
    
    game = SnakeGame(12, 8)
    
    while not game.game_over:
        game.display()
        
        # 간단한 AI: 먹이 방향으로 이동
        head_x, head_y = game.snake[0]
        food_x, food_y = game.food
        
        # 먹이 방향 계산
        if food_x > head_x and game.direction != (-1, 0):  # 오른쪽
            game.change_direction((1, 0))
        elif food_x < head_x and game.direction != (1, 0):  # 왼쪽
            game.change_direction((-1, 0))
        elif food_y > head_y and game.direction != (0, -1):  # 아래
            game.change_direction((0, 1))
        elif food_y < head_y and game.direction != (0, 1):  # 위
            game.change_direction((0, -1))
        
        game.move_snake()
        time.sleep(0.5)  # 0.5초 대기
        
        # 키 입력 체크 (종료용)
        try:
            if WINDOWS and msvcrt.kbhit():
                msvcrt.getch()
                break
        except:
            pass
    
    game.display()
    if game.game_over:
        print("🤖 AI 뱀이 게임 오버되었습니다!")
    print(f"AI 최종 점수: {game.score}")

def ascii_snake_art():
    """
    ASCII 아트로 뱀 그리기
    """
    snake_art = """
    🐍 SNAKE GAME 🐍
    
       /^\/^\\
     _|__|  O|
\/  /~     \_/ \\
 \____|__________/  \\
        \_______      \\
                `\     \\                 \\
                  |     |                  \\
                 /      /                    \\
                /     /                       \\\\
              /      /                         \\ \\
             /     /                            \\  \\
           /     /             _----_            \\   \\
          /     /           _-~      ~-_         |   |
         (      (        _-~    _--_    ~-_     _/   |
          \\      ~-____-~    _-~    ~-_    ~-_-~    /
            ~-_           _-~          ~-_       _-~
               ~--______-~                ~-___-~
    """
    print(snake_art)

def main():
    """
    메인 메뉴
    """
    while True:
        ascii_snake_art()
        print("="*50)
        print("🐍 뱀 게임 메뉴 🐍")
        print("="*50)
        print("1. 게임 플레이 (수동 조작)")
        print("2. 자동 플레이 데모")
        print("3. 게임 규칙 보기")
        print("4. 게임 종료")
        print("-"*50)
        
        choice = input("선택하세요 (1-4): ")
        
        if choice == '1':
            simple_snake_game()
        elif choice == '2':
            auto_snake_demo()
        elif choice == '3':
            show_rules()
        elif choice == '4':
            print("👋 게임을 종료합니다!")
            break
        else:
            print("❌ 올바른 번호를 선택해주세요!")
        
        input("\n계속하려면 엔터를 누르세요...")

def show_rules():
    """
    게임 규칙 설명
    """
    print("\n" + "="*50)
    print("🐍 뱀 게임 규칙 🐍")
    print("="*50)
    print("1. 뱀(●○○)을 조작하여 먹이(🍎)를 먹습니다")
    print("2. 먹이를 먹으면 뱀이 길어지고 점수가 올라갑니다")
    print("3. 벽이나 자신의 몸통에 부딪히면 게임 오버!")
    print("4. 조작법:")
    print("   W: 위로 이동")
    print("   A: 왼쪽으로 이동") 
    print("   S: 아래로 이동")
    print("   D: 오른쪽으로 이동")
    print("   Q: 게임 종료")
    print("5. 뱀은 반대 방향으로 갈 수 없습니다")
    print("6. 먹이를 먹을 때마다 10점 획득!")
    print("-"*50)

if __name__ == "__main__":
    main()
