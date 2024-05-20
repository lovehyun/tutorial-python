import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Hello PyGame')

image1 = pygame.image.load('./images/butterfly1.png')
image1 = pygame.transform.scale(image1, (64, 64))

# 화면 색상 설정
screen.fill((255, 255, 255))

# 이미지 초기 위치 설정
x = screen.get_width() / 2 - image1.get_width() / 2
y = screen.get_height() / 2 - image1.get_height() / 2

# 이동 속도 설정
speed = 1

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # 화면 업데이트
    screen.fill((255, 255, 255))
    screen.blit(image1, (x, y))
    pygame.display.update()

pygame.quit()
