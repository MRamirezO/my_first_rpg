import sys, pygame
from settings import *
from player import *
pygame.init()

FramePerSec = pygame.time.Clock()
size = SCREEN_WIDTH, SCREEN_HEIGHT

screen = pygame.display.set_mode(size)

P1 = Player()

while True:
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
     
    screen.fill(GREEN)
    P1.draw(screen)
         
    pygame.display.update()
    FramePerSec.tick(FPS)