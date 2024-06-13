import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Web Game Example')

clock = pygame.time.Clock()
color = (0, 128, 255)
rect = pygame.Rect(30, 30, 60, 60)

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect.x -= 5
        if keys[pygame.K_RIGHT]:
            rect.x += 5
        if keys[pygame.K_UP]:
            rect.y -= 5
        if keys[pygame.K_DOWN]:
            rect.y += 5

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, color, rect)
        pygame.display.flip()
        clock.tick(30)

        yield pygame.surfarray.array3d(screen)

if __name__ == '__main__':
    game_loop()
