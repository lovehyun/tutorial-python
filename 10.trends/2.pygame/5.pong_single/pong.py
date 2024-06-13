import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Single Player Pong')

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 객체 설정
paddle_width = 10
paddle_height = 100
ball_size = 10

player_pos = [50, SCREEN_HEIGHT // 2 - paddle_height // 2]
ai_pos = [SCREEN_WIDTH - 50 - paddle_width, SCREEN_HEIGHT // 2 - paddle_height // 2]
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_velocity = [5, 5]

clock = pygame.time.Clock()

# 점수 설정
player_score = 0
ai_score = 0
font = pygame.font.SysFont("monospace", 35)

def ai_move():
    if ai_pos[1] + paddle_height / 2 < ball_pos[1]:
        ai_pos[1] += 5
    elif ai_pos[1] + paddle_height / 2 > ball_pos[1]:
        ai_pos[1] -= 5

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= 5
    if keys[pygame.K_s] and player_pos[1] < SCREEN_HEIGHT - paddle_height:
        player_pos[1] += 5

    ai_move()

    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - ball_size:
        ball_velocity[1] = -ball_velocity[1]

    if (ball_pos[0] <= player_pos[0] + paddle_width and player_pos[1] <= ball_pos[1] <= player_pos[1] + paddle_height) or \
       (ball_pos[0] >= ai_pos[0] - ball_size and ai_pos[1] <= ball_pos[1] <= ai_pos[1] + paddle_height):
        ball_velocity[0] = -ball_velocity[0]

    if ball_pos[0] < 0:
        ai_score += 1
        ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        ball_velocity = [5, 5]
    elif ball_pos[0] > SCREEN_WIDTH:
        player_score += 1
        ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        ball_velocity = [-5, -5]

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (ai_pos[0], ai_pos[1], paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_pos[0], ball_pos[1], ball_size, ball_size))

    player_text = font.render(f"Player: {player_score}", True, WHITE)
    ai_text = font.render(f"AI: {ai_score}", True, WHITE)
    screen.blit(player_text, (50, 10))
    screen.blit(ai_text, (SCREEN_WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
