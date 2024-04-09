import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Hello PyGame')

image1 = pygame.image.load('./images/butterfly1.png')
image1 = pygame.transform.scale(image1, (64, 64))

# screen.fill((0, 0, 0))
screen.fill((255, 255, 255))

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    # screen.blit(image1, (0, 0))
    screen.blit(image1, (screen.get_width()/2 - image1.get_width()/2, screen.get_height()/2 - image1.get_height()/2))
    pygame.display.update()

pygame.quit()
