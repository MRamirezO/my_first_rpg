import pygame, time
from pygame.locals import *
from settings import *

# Tile types:

WATER = 0
GREEN_GRASS = 1
GROUND = 2
WALL = 3
CASTLE_WALL = 4
WOODEN_FLOOR = 5
DOOR = 6
LAVA = 7
POISON = 8
CARPET = 9

class Tile(pygame.sprite.Sprite):
    def __init__(self,tile_type,x,y):
        super().__init__() 
        self.image = pygame.image.load(f"sprites/tiles/{tile_type}.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.tile_type = tile_type
        self.collide = False
 
    def update(self):
        pass
        

    def animate(self):
        pass
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)  

class Obstacle(Tile):

    def __init__(self,tile_type,x,y):
        super().__init__(tile_type,x,y) 
        self.collide = True


class Trap(Tile):

    def __init__(self,tile_type,x,y):
        super().__init__(tile_type,x,y) 
        self.damage = 10
