import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    x_pos = 0
    clock = pygame.time.Clock()
    v = 200
    fps = 90
    while running:
        screen.fill(GREEN)
        pygame.draw.circle(screen, RED, (x_pos, 400), 20)
        x_pos += clock.tick(fps) * v / 1000
        if x_pos >= 800:
            x_pos = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()


