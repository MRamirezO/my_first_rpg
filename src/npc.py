import pygame, random, time
from settings import *
from pygame.locals import *
from misc import *

MOVE_RIGHT = 1
MOVE_LEFT = 2
MOVE_UP = 3
MOVE_DOWN = 4



class NPC(pygame.sprite.Sprite):
    dialog = None
    def __init__(self, name, position, dialogs):
        super().__init__() 
        self.image = pygame.image.load("assets/sprites/npc_1.png")
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.topleft= position
        self.idle_frame_start = time.time()
        self.dialog_index = 1
        self.dialogs = dialogs

    def talk(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key==K_SPACE:
                    
                    if self.dialog_index == len(self.dialogs):
                        self.dialog = None
                        self.dialog_index = 1
                    else:
                        self.dialog_index += 1
                        self.dialog.update_text([self.dialogs[self.dialog_index - 1]])

    def move(self):
        if self.direction == MOVE_RIGHT:
            self.rect.move_ip(5, 0)
        elif self.direction == MOVE_LEFT:
            self.rect.move_ip(-5, 0)
        elif self.direction == MOVE_UP:
            self.rect.move_ip(0, -5)
        elif self.direction == MOVE_DOWN:
            self.rect.move_ip(0, 5)


        if self.rect.right >= SCREEN_WIDTH:        
            self.direction = MOVE_LEFT
        if self.rect.left <= 0:
            self.direction = MOVE_RIGHT
        if self.rect.bottom >= SCREEN_HEIGHT:        
            self.direction = MOVE_UP
        if self.rect.top <= 0:
            self.direction = MOVE_DOWN
        
        if time.time() - self.turn_time > 3.0: 
            self.direction = random.randint(1,4)
            self.turn_time = time.time()
        self.animate()

    def animate(self):
        if time.time() - self.idle_frame_start > 0.5:
            self.image = pygame.transform.flip(self.image, True, False)
            self.idle_frame_start = time.time()


 
    def draw(self, surface):
        self.animate()
        surface.blit(self.image, self.rect) 