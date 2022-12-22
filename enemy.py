import pygame, random, time
from settings import *

MOVE_RIGHT = 5
MOVE_LEFT = -5

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("sprites/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center= (160, 520)
        self.direction = MOVE_RIGHT
        self.idle_frame_start = time.time()
 
      def move(self):
        self.rect.move_ip(self.direction, 0)
        if self.rect.right >= SCREEN_WIDTH:        
            self.direction = MOVE_LEFT
        if self.rect.left <= 0:
            self.direction = MOVE_RIGHT
        if time.time() - self.idle_frame_start > 0.5: 
            self.image = pygame.transform.flip(self.image, True, False)
            self.idle_frame_start = time.time()
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) 