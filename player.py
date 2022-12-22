import pygame, time
from pygame.locals import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("sprites/main_character_mid.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.idle_frame_start = time.time()
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                    self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                    self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
        if time.time() - self.idle_frame_start > 0.5: # if the time difference is bigger than 0.8s
            self.image = pygame.transform.flip(self.image, True, False)
            self.idle_frame_start = time.time() # reset the start time
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)  