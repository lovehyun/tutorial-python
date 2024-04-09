import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Hello PyGame')

image1 = pygame.image.load('./images/football1.png')

# screen.fill((0, 0, 0))
screen.fill((255, 255, 255))

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.blit(image1, (0, 0))
    pygame.display.update()

pygame.quit()
