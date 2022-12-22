import sys, pygame
from settings import *
from player import *
from background import *
from enemy import *
from pygame import mixer

pygame.init()

FramePerSec = pygame.time.Clock()
size = SCREEN_WIDTH, SCREEN_HEIGHT

screen = pygame.display.set_mode(size)

background = Background('sprites/bg_grass.png', [0,0])

mixer.init()
mixer.music.load('music/map_theme.mp3')
mixer.music.play(-1)
enemy_hit = pygame.mixer.Sound("sfx/die.wav")

P1 = Player()
E1 = Enemy()

while True:
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()
    E1.move()
     
    screen.fill(BLUE)
    background.draw(screen)
    P1.draw(screen)
    E1.draw(screen)

    if pygame.sprite.collide_rect(P1, E1):
        mixer.music.stop()
        enemy_hit.play()
        time.sleep(5)
        pygame.quit()
        sys.exit()      
         
    pygame.display.update()
    FramePerSec.tick(FPS)