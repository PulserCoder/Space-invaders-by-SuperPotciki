import random
import sys
import pygame
import os


class Bullet:
    def __init__(self, screen, coords, speed=3, vector=-1):
        self.coords = coords
        self.vector = vector
        self.speed = speed
        self.screen = screen

    def move(self):
        self.coords = (self.coords[0], self.coords[1] + self.vector * self.speed)

    def render(self):
        pygame.draw.circle(self.screen, 'white', self.coords, 5)

class HealthPoint:
        def __init__(self, hp):
            self.hp = hp

        def render(self):
            heart.rect.x, heart.rect.y = 600, 20


class Enemy:
    def __init__(self, hp, pos_x, pos_y):
        self.hp = hp
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.t = True

    def render(self):
        pygame.draw.circle(screen, RED, (self.pos_x, self.pos_y), 20)

    def die(self):
        self.t = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
x_pos = 400
v = 5
fps = 90
bullets = []
timeout = 900

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

all_sprites = pygame.sprite.Group()
heart = pygame.sprite.Sprite()
heart.image = load_image("heart3.png")
heart.rect = heart.image.get_rect()
all_sprites.add(heart)
health = 3
hp = HealthPoint(health)
em1 = Enemy(3, 400, 100)



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
            if x_pos <= 0:
                x_pos = 0 + v
            x_pos -= v
        if keys[pygame.K_RIGHT]:
            if x_pos >= 800:
                x_pos = 800 - v
            x_pos += v
        if keys[pygame.K_SPACE] and not timeout != 900:
            bullet = Bullet(screen, (x_pos, 700))
            bullets.append(bullet)
            timeout = 0
        pygame.draw.circle(screen, RED, (x_pos, 700), 20)
        if em1.t != False:
            em1.render()
        for i in bullets:
            i.render()
            i.move()
            if i.coords == (em1.pos_x, em1.pos_y):
                em1.die()
        if hp.hp == 3:
            filename = 'heart3.png'
        elif hp.hp == 2:
            filename = 'heart2.png'
        elif hp.hp == 1:
            filename = 'heart.png'
        heart.image = load_image(filename)
        all_sprites.draw(screen)
        hp.render()

        pygame.display.flip()
        if timeout != 900:
            timeout += fps
        clock.tick(fps)
    pygame.quit()

# if event.type == pygame.KEYDOWN:
#    if event.key == pygame.K_RIGHT:
#        x_pos = ship.movement_ship_right()
#    elif event.key == pygame.K_LEFT:
#        x_pos = ship.movement_ship_left()
