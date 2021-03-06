import os
import pygame
import random
import sqlite3
import sys
import time
from uuid import getnode


class MainMenu:
    def __init__(self):
        pygame.init()
        size = 800, 800
        self.screen = pygame.display.set_mode(size)
        self.mac = getnode()
        db = sqlite3.connect('base.db')
        cur = db.cursor()
        res = cur.execute("""SELECT * FROM users WHERE mac=?""", (self.mac,)).fetchone()
        if res is None:
            cur.execute("INSERT INTO users(mac, level) VALUES (? , ?)", (self.mac, 1))
            db.commit()
            db.close()
            self.screen.blit(load_image('menu_1.jpg'), (0, 0))
        else:
            db.close()
            if res[1] == 1:
                self.screen.blit(load_image('menu_1.jpg'), (0, 0))
            if res[1] == 2:
                self.screen.blit(load_image('menu_2.jpg'), (0, 0))
            if res[1] >= 3:
                self.screen.blit(load_image('menu.jpg'), (0, 0))

    def start(self):
        running = True
        db = sqlite3.connect('base.db')
        cur = db.cursor()
        res = cur.execute("""SELECT level FROM users WHERE mac=?""", (self.mac,)).fetchone()
        db.close()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    print(x, y)
                    if 425 < y and y < 705 and 60 < x and x < 265 and res[0] >= 1:
                        self.screen.blit(load_image('listening.png'), (0, 0))
                        pygame.display.flip()
                        time.sleep(5)
                        game = Level(60, 20)
                        game.start()
                        print(1)
                    if 425 < y and y < 705 and 300 < x and x < 500 and res[0] >= 2:
                        game = Level(100, 40)
                        game.start()
                    if 425 < y and y < 705 and 530 < x and x < 738 and res[0] >= 3:
                        game = Level(100, 45, boss=True)
                        game.start()
            pygame.display.flip()


class Level:
    def __init__(self, time, ships, boss=False):
        global main_body
        self.time = time
        self.mac = getnode()
        self.timeout = 900
        self.leveltime = 0
        self.won = False
        self.ships = ships
        size = width, height = 800, 800
        self.screen = pygame.display.set_mode(size)
        self.heart = pygame.sprite.Sprite()
        self.heart.image = load_image("heart3.png")
        self.heart.rect = self.heart.image.get_rect()
        all_sprites.add(self.heart)
        self.health = 3
        self.hp = HealthPoint(self.health)
        self.ship = Ship(self.screen)
        self.enemycooldown = self.time // self.ships
        self.spawncounter = 0
        self.isboss = boss
        self.bossalive = False
        self.bosscooldown = 50
        self.bosscounter = 0
        em = Enemy(self.screen, 3, random.randrange(50, 750), 0, speed=2)
        enemies.append(em)

    def start(self):
        pygame.init()
        clock = pygame.time.Clock()
        sound = pygame.mixer.Sound('SoundTrack_1.mp3')
        sound2 = pygame.mixer.Sound('boss.mp3')
        sound3 = pygame.mixer.Sound('beat.mp3')
        sound.play()
        running = True
        while running:
            self.screen.fill(GREEN)
            self.screen.blit(load_image('phone.jpg'), (0, 0))
            all_sprites.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if (self.time - (self.leveltime // 9000)) == 0:
                db = sqlite3.connect('base.db')
                cur = db.cursor()
                level = cur.execute("""SELECT level FROM users WHERE mac = ?""", (self.mac,)).fetchone()[0]
                cur.execute("""
                UPDATE users
                SET level = ?
                WHERE mac = ?
                """, (level + 1, self.mac))
                db.commit()
                break
            if self.hp.hp == 0:
                break
            if keys[pygame.K_LEFT]:
                self.ship.move(left)
            if keys[pygame.K_RIGHT]:
                self.ship.move(right)
            if keys[pygame.K_SPACE] and not self.timeout != 1800:
                self.ship.shoot()
                self.timeout = 0
            self.spawning()
            if self.isboss and (self.time - (self.leveltime // 9000)) == self.time // 2:
                self.boss = Boss(self.screen, 3, 400, 0)
                self.isboss = False
                self.bossalive = True
                enemies.append((self.boss))
                sound2.play()
            for i in bullets:
                i.render()
                i.move()
                if i.coords[1] > 800 or i.coords[1] <= 0:
                    i.isactive = False
                    bullets.remove(i)
                if i.coords in self.ship.hitbox and i.vector == 1 and i.isactive:
                    self.hp.hp -= 1
                    sound3.play()
                    bullets.remove(i)
                    i.isactive = False
                for j in enemies:
                    if j.t != False:
                        j.render()
                    if i.coords in j.hitbox and j.t and i.vector == -1 and i.isactive:
                        j.die()
                        i.isactive = False
                        bullets.remove(i)
                        if self.bossalive == False:
                            all_sprites.remove(j.enemy)
                        else:
                            if j != self.boss or self.boss.t == False:
                                all_sprites.remove(j.enemy)
            for i in enemies:
                if i.t:
                    i.cooldownupdate()
                if not self.bossalive:
                    i.move()
                    i.hitboxupdate()
                if self.bossalive:
                    if i.t and not i.isboss:
                        if i.isboss:
                            print('???????? ??????????????????, ??????????????', self.bosscounter)
                        i.move()
                        i.hitboxupdate()
                    if i.t and i.isboss:
                        if self.bosscounter != self.bosscooldown:
                            self.bosscounter += 1
                        else:
                            i.move()
                            i.hitboxupdate()
                if i.pos_y > 830:
                    i.vector = 0
                    enemies.remove(i)
                    self.hp.hp -= 1
            if self.hp.hp >= 3:
                filename = 'heart3.png'
            elif self.hp.hp == 2:
                filename = 'heart2.png'
            elif self.hp.hp == 1:
                filename = 'heart.png'
            font = pygame.font.Font(None, 50)
            text = font.render(str(self.time - (self.leveltime // 9000)), True, ('WHITE'))
            self.screen.blit(text, (20, 20))
            self.heart.image = load_image(filename)
            self.ship.render()
            all_sprites.draw(self.screen)
            self.hp.render()
            self.heart.rect.x, self.heart.rect.y = 600, 20
            pygame.display.flip()
            if self.timeout != 1800:
                self.timeout += fps
            self.leveltime += fps
            clock.tick(fps)
        pygame.quit()
        self.clean()
        main_body.__init__()
        main_body.start()

    def clean(self):
        bullets.clear()
        for i in enemies:
            all_sprites.remove(i.enemy)
        enemies.clear()

    def spawning(self):
        if self.spawncounter != self.enemycooldown * 100:
            self.spawncounter += 1
            return
        else:
            self.spawncounter = 0
        a = True
        while a:
            pos_x = random.randrange(50, 750)
            for i in enemies:
                if pos_x in i.hitbox:
                    a = True
                else:
                    a = False
            if not a:
                break
        em = Enemy(self.screen, 3, pos_x, 0, speed=2)
        enemies.append(em)


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
        ship.rect.x = self.pos_x - 20
        ship.rect.y = self.pos_y

    def shoot(self):
        bullet = Bullet(self.screen, (self.pos_x, self.pos_y))
        bullets.append(bullet)

    def hitboxupdate(self):
        self.hitbox = []
        for i in range(self.pos_x - 20, self.pos_x + 20):
            for j in range(self.pos_y - 20, self.pos_y + 20):
                self.hitbox.append((i, j))


class Bullet:
    def __init__(self, screen, coords, speed=6, vector=-1):
        self.isactive = True
        self.pos_y = coords[1]
        self.coords = coords
        self.pos_x = coords[0]
        self.pos_y = coords[1]
        self.vector = vector
        self.speed = speed
        self.screen = screen

    def move(self):
        self.coords = (self.coords[0], self.coords[1] + self.vector * self.speed)

    def render(self):
        pygame.draw.circle(self.screen, 'white', self.coords, 3)


class HealthPoint:
    def __init__(self, hp):
        self.hp = hp

    def render(self):
        pass


class Enemy:
    def __init__(self, screen, hp, pos_x, pos_y, speed=4, vector=1, shootrate=5400, isboss=False):
        enemy_image = load_image('enemy.png')
        self.enemy = pygame.sprite.Sprite(all_sprites)
        self.enemy.image = enemy_image
        self.enemy.rect = (self.enemy.image.get_rect())
        self.hp = hp
        self.isboss = isboss
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
        self.enemy.rect.x = self.pos_x - 20
        self.enemy.rect.y = self.pos_y - 30

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


class Boss(Enemy):
    def __init__(self, screen, hp, pos_x, pos_y, speed=1, shootrate=21600, isboss=True):
        super().__init__(screen, hp, pos_x, pos_y, speed=1, shootrate=9000, isboss=True)
        self.hp = 25
        self.cooldown = 2
        self.countmover = 0
        enemy_image = load_image('boss.png')
        self.enemy = pygame.sprite.Sprite(all_sprites)
        self.enemy.image = enemy_image
        self.enemy.rect = (self.enemy.image.get_rect())

    def shoot(self):
        bullet1 = Bullet(self.screen, (self.pos_x - 30, self.pos_y), 3, 1)
        bullet2 = Bullet(self.screen, (self.pos_x, self.pos_y), 3, 1)
        bullet3 = Bullet(self.screen, (self.pos_x + 30, self.pos_y), 3, 1)
        bullets.append(bullet1)
        bullets.append(bullet2)
        bullets.append(bullet3)

    def move(self):
        if self.pos_y <= 300:
            self.pos_y += self.speed * self.vector
        else:
            pass

    def die(self):
        if self.hp != 1:
            self.hp -= 1
        else:
            self.t = False

    def hitboxupdate(self):
        self.hitbox = []
        for i in range(self.pos_x - 40, self.pos_x + 40):
            for j in range(self.pos_y - 40, self.pos_y + 40):
                self.hitbox.append((i, j))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
x_pos = 400
fps = 90
left = -5
right = 5
all_sprites = pygame.sprite.Group()
bullets = []
enemies = []


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"???????? ?? ???????????????????????? '{fullname}' ???? ????????????")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
ship_image = load_image('ship.png')
ship = pygame.sprite.Sprite(all_sprites)
ship.image = ship_image
ship.rect = (ship.image.get_rect())

main_body = MainMenu()
main_body.start()

# print('# ?????????????? ???????????????????? ?????????????????? ?????????? ????????????')
