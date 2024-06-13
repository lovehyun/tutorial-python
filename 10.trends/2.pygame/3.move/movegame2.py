import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Arcade Game')

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 플레이어 설정
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
player_speed = 10

# 장애물 설정
enemy_size = 50
enemy_pos = [random.randint(0, SCREEN_WIDTH-enemy_size), 0]
enemy_speed = 5

# 체력 설정
player_health = 100
health_bar_length = 100
health_bar_height = 10

# 점수 설정
score = 0
font = pygame.font.SysFont("monospace", 35)

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 5 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def draw_health_bar(surface, x, y, health, max_health):
    if health < 0:
        health = 0
    health_ratio = health / max_health
    pygame.draw.rect(surface, RED, (x, y, health_bar_length, health_bar_height))
    pygame.draw.rect(surface, GREEN, (x, y, health_bar_length * health_ratio, health_bar_height))

def game_over_screen():
    global player_health, score
    screen.fill(BLACK)
    text = font.render("Game Over! Your score was: {}".format(score), True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    text = font.render("Press Y to Restart or N to Quit", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + text.get_height()//2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    player_health = 100
                    score = 0
                    return True
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
    return False

clock = pygame.time.Clock()
enemy_list = [enemy_pos]

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed

    screen.fill(BLACK)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)

    if collision_check(enemy_list, player_pos):
        player_health -= 1
        if player_health <= 0:
            if not game_over_screen():
                running = False

    draw_enemies(enemy_list)
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
    draw_health_bar(screen, 10, 10, player_health, 100)

    text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(text, (10, 30))

    clock.tick(30)
    pygame.display.update()

print("Game Over! Your score was:", score)
pygame.quit()
