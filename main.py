import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
x_pos = 400
v = 5
fps = 90


def check_gran(x, v):
    if x >= 800:
        return -v
    if x <= 0:
        return -v
    return v


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_pos -= v
            if x_pos < 0:
                x_pos += 0 + v
        if keys[pygame.K_RIGHT]:
            x_pos += v
            if x_pos > 800:
                print(x_pos)
                x_pos = 800 - v
            # if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_RIGHT:
            #        x_pos = ship.movement_ship_right()
            #    elif event.key == pygame.K_LEFT:
            #        x_pos = ship.movement_ship_left()
        pygame.draw.circle(screen, RED, (x_pos, 700), 20)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
