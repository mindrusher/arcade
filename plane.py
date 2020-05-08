import pygame
import random
import time
import os

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (460,240)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('plane.png')
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(40,round(SCREEN_HEIGHT/2)))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            move_sound.play()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            move_sound.play()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missle.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        global counter
        f1 = pygame.font.Font('Pixel-Font.ttf', 30)
        text = f1.render('Счет: {0}'.format(counter), 1, (0, 0, 255))

        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            counter = counter + 1

        screen.blit(text, (20, 560))

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self):        
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
                      
counter = 0

pygame.mixer.init()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()

pygame.mixer.music.load(r"Endless Cyber Runner.mp3")
pygame.mixer.music.play(loops=-1)

move_sound = pygame.mixer.Sound("fly.wav")
move_sound.set_volume(.15)
collision_sound = pygame.mixer.Sound("explosion.wav")

running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)    
    
    clouds.update()
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(player.surf, player.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_sound.stop()
        collision_sound.play()
        time.sleep(0.5)
        running = False

    pygame.display.flip()

    clock.tick(30)