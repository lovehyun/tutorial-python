import pygame
import socket
import threading

# 서버 설정
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# 소켓 생성 및 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Server: {message}")
        except:
            break

threading.Thread(target=receive_messages).start()

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Multiplayer Pong')

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 객체 설정
paddle_width = 10
paddle_height = 100
ball_size = 10

player1_pos = [50, SCREEN_HEIGHT // 2 - paddle_height // 2]
player2_pos = [SCREEN_WIDTH - 50 - paddle_width, SCREEN_HEIGHT // 2 - paddle_height // 2]
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_velocity = [5, 5]

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_pos[1] > 0:
        player1_pos[1] -= 5
    if keys[pygame.K_s] and player1_pos[1] < SCREEN_HEIGHT - paddle_height:
        player1_pos[1] += 5
    if keys[pygame.K_UP] and player2_pos[1] > 0:
        player2_pos[1] -= 5
    if keys[pygame.K_DOWN] and player2_pos[1] < SCREEN_HEIGHT - paddle_height:
        player2_pos[1] += 5

    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - ball_size:
        ball_velocity[1] = -ball_velocity[1]

    if (ball_pos[0] <= player1_pos[0] + paddle_width and player1_pos[1] <= ball_pos[1] <= player1_pos[1] + paddle_height) or \
       (ball_pos[0] >= player2_pos[0] - ball_size and player2_pos[1] <= ball_pos[1] <= player2_pos[1] + paddle_height):
        ball_velocity[0] = -ball_velocity[0]

    if ball_pos[0] < 0 or ball_pos[0] > SCREEN_WIDTH:
        ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        ball_velocity = [5, 5]

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player1_pos[0], player1_pos[1], paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (player2_pos[0], player2_pos[1], paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_pos[0], ball_pos[1], ball_size, ball_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
client_socket.close()
