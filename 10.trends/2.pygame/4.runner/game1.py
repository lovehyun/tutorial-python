import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Endless Runner Game')

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 이미지 로드 및 크기 조절
background = pygame.image.load('images/forest.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
character = pygame.image.load('images/yoshi.jpg')
character = pygame.transform.scale(character, (50, 50))
enemy = pygame.image.load('images/boo.jpg')
enemy = pygame.transform.scale(enemy, (50, 50))

# 배경 설정
background_x1 = 0
background_x2 = SCREEN_WIDTH

# 높이 설정
ground_level = -200

# 플레이어 설정
character_size = 50
character_pos = [100, SCREEN_HEIGHT + ground_level]
character_y_velocity = 0
gravity = 1
jump_strength = 15
is_jumping = False

# 적 설정
enemy_size = 50
enemy_pos = [SCREEN_WIDTH, SCREEN_HEIGHT + ground_level]
enemy_speed = 10

# 점수 설정
score = 0
font = pygame.font.SysFont("monospace", 35)

def reset_enemy():
    return [SCREEN_WIDTH, SCREEN_HEIGHT + ground_level]

def detect_collision(character_pos, enemy_pos):
    c_x = character_pos[0]
    c_y = character_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= c_x and e_x < (c_x + character_size)) or (c_x >= e_x and c_x < (e_x + enemy_size)):
        if (e_y >= c_y and e_y < (c_y + character_size)) or (c_y >= e_y and c_y < (e_y + enemy_size)):
            return True
    return False

clock = pygame.time.Clock()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                character_y_velocity = -jump_strength

    # 배경 움직임
    background_x1 -= 5
    background_x2 -= 5

    if background_x1 <= -SCREEN_WIDTH:
        background_x1 = SCREEN_WIDTH
    if background_x2 <= -SCREEN_WIDTH:
        background_x2 = SCREEN_WIDTH

    # 캐릭터 점프
    if is_jumping:
        character_pos[1] += character_y_velocity
        character_y_velocity += gravity

        if character_pos[1] >= SCREEN_HEIGHT + ground_level:
            character_pos[1] = SCREEN_HEIGHT + ground_level
            is_jumping = False

    # 적 이동
    enemy_pos[0] -= enemy_speed
    if enemy_pos[0] < 0:
        enemy_pos = reset_enemy()
        score += 1

    # 충돌 감지
    if detect_collision(character_pos, enemy_pos):
        running = False

    # 화면 그리기
    screen.fill(BLACK)
    screen.blit(background, (background_x1, 0))
    screen.blit(background, (background_x2, 0))
    screen.blit(character, (character_pos[0], character_pos[1]))
    screen.blit(enemy, (enemy_pos[0], enemy_pos[1]))

    # 점수 표시
    text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(text, (10, 10))

    clock.tick(30)
    pygame.display.update()

# 게임 오버 화면
while True:
    screen.fill(BLACK)
    text = font.render("Game Over! Your score was: {}".format(score), True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    text = font.render("Press Y to Restart or N to Quit", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + text.get_height()))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                # 초기화
                character_pos = [100, SCREEN_HEIGHT + ground_level]
                character_y_velocity = 0
                enemy_pos = reset_enemy()
                score = 0
                running = True
                break
            elif event.key == pygame.K_n:
                pygame.quit()
                sys.exit()
    if running:
        break
