import sys, pygame
from settings import *
from player import *
from background import *
from enemy import *

pygame.init()

FramePerSec = pygame.time.Clock()
size = SCREEN_WIDTH, SCREEN_HEIGHT

screen = pygame.display.set_mode(size)

background = Background('sprites/bg_grass.png', [0,0])

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
         
    pygame.display.update()
    FramePerSec.tick(FPS)