import os
import sys

import pygame

class Level:
    def __init__(self, time, ships):
        self.time = time
        self.timeout = 900
        self.ships = ships
        self.all_sprites = pygame.sprite.Group()
        size = width, height = 800, 800
        self.screen = pygame.display.set_mode(size)
        self.heart = pygame.sprite.Sprite()
        self.heart.image = load_image("heart3.png")
        self.heart.rect = self.heart.image.get_rect()
        self.all_sprites.add(self.heart)
        self.health = 3
        self.hp = HealthPoint(self.health)
        self.em1 = Enemy(self.screen, 3, 400, 100, speed=2)
        enemies.append(self.em1)
        self.ship = Ship(self.screen)

    def start(self):
        pygame.init()
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill(GREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.ship.move(left)
            if keys[pygame.K_RIGHT]:
                self.ship.move(right)
            if keys[pygame.K_SPACE] and not self.timeout != 1800:
                self.ship.shoot()
                self.timeout = 0
            if self.em1.t != False:
                self.em1.render()
            for i in bullets:
                i.render()
                i.move()
                if i.coords in self.ship.hitbox and i.vector == 1 and i.isactive:
                    self.hp.hp -= 1
                    bullets.remove(i)
                    i.isactive = False
                for j in enemies:
                    if i.coords in j.hitbox and j.t and i.vector == -1 and i.isactive:
                        self.em1.die()
                        i.isactive = False
                        bullets.remove(i)
            for i in enemies:
                if i.t:
                    i.cooldownupdate()
                if i.t:
                    i.move()
                    i.hitboxupdate()
                if i.pos_y > 830:
                    i.vector = 0
                    enemies.remove(i)
                    self.hp.hp -= 1
            if self.hp.hp == 3:
                filename = 'heart3.png'
            elif self.hp.hp == 2:
                filename = 'heart2.png'
            elif self.hp.hp == 1:
                filename = 'heart.png'
            self.heart.image = load_image(filename)
            self.ship.render()
            self.all_sprites.draw(self.screen)
            self.hp.render()
            self.heart.rect.x, self.heart.rect.y = 600, 20
            pygame.display.flip()
            if self.timeout != 1800:
                self.timeout += fps
            clock.tick(fps)
        pygame.quit()


class Ship:
    def __init__(self, screen):
        self.screen = screen
        self.pos_x = 400
        self.pos_y = 700
        self.coords = (self.pos_x, self.pos_y)
        self.hitbox = []
        for i in range(self.pos_x - 20, self.pos_x + 20):
            for j in range(self.pos_y - 20, self.pos_y + 20):
                self.hitbox.append((i, j))

    def move(self, side):
        if self.pos_x + side > 20 and self.pos_x + side < 780:
            self.pos_x += side
            self.hitboxupdate()

    def render(self):
        pygame.draw.circle(self.screen, RED, (self.pos_x, self.pos_y), 20)

    def shoot(self):
        bullet = Bullet(self.screen, (self.pos_x, self.pos_y))
        bullets.append(bullet)

    def hitboxupdate(self):
        self.hitbox = []
        for i in range(self.pos_x - 20, self.pos_x + 20):
            for j in range(self.pos_y - 20, self.pos_y + 20):
                self.hitbox.append((i, j))



class Bullet:
    def __init__(self, screen, coords, speed=3, vector=-1):
        self.isactive = True
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
        pass


class Enemy:
    def __init__(self, screen, hp, pos_x, pos_y, speed=4, vector=1, shootrate=5400):
        self.hp = hp
        self.screen = screen
        self.shootrate = shootrate
        self.cooldown = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.vector = vector
        self.t = True
        self.hitbox = []
        for i in range(self.pos_x - 20, self.pos_x + 20):
            for j in range(self.pos_y - 20, self.pos_y + 20):
                self.hitbox.append((i, j))

    def cooldownupdate(self):
        if self.cooldown < self.shootrate:
            self.cooldown += 90
        elif self.cooldown >= self.shootrate:
            self.cooldown = 0
            self.shoot()

    def render(self):
        pygame.draw.circle(self.screen, RED, (self.pos_x, self.pos_y), 20)

    def die(self):
        self.t = False

    def move(self):
        if self.t:
            self.pos_y += self.speed * self.vector

    def hitboxupdate(self):
        self.hitbox = []
        for i in range(self.pos_x - 20, self.pos_x + 20):
            for j in range(self.pos_y - 20, self.pos_y + 20):
                self.hitbox.append((i, j))

    def shoot(self):
        bullet = Bullet(self.screen, (self.pos_x, self.pos_y), 3, 1)
        bullets.append(bullet)



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
x_pos = 400
fps = 90
left = -5
right = 5
bullets = []
enemies = []


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


game = Level(180, 50)
game.start()