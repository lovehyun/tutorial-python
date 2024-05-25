# 1. 기본 화면에서 snake 이동 가능
# 2. 화면 내에서만 이동 가능하고 벽에 부딛치면 game over

import pygame
import time
import sys

pygame.init()

# 색 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)

# 화면 크기
dis_width = 800
dis_height = 600

# 화면 설정
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Simple Snake Movement')

# 시계 설정
clock = pygame.time.Clock()
snake_block = 20
snake_speed = 10

# 폰트 설정
font_style = pygame.font.SysFont("bahnschrift", 25)

# 좌표 표시 함수
def show_coordinates(x, y):
    value = font_style.render("Coordinates: " + str(x) + ", " + str(y), True, black)
    dis.blit(value, [20, 0])

# 게임 종료 메시지 함수
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - 100, dis_height / 2])

# 게임 루프
def gameLoop():
    x1 = int (dis_width / 2)
    y1 = int (dis_height / 2)

    x1_change = 0
    y1_change = 0

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over = True

        dis.fill(white)
        pygame.draw.rect(dis, black, [x1, y1, snake_block, snake_block])
        show_coordinates(x1, y1)
        pygame.display.update()

        clock.tick(snake_speed)

    dis.fill(white)
    message("Game Over!", red)
    pygame.display.update()
    time.sleep(2)
    
    pygame.quit()
    sys.exit()

gameLoop()
