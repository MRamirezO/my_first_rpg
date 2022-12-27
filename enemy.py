import pygame, random, time
from settings import *

MOVE_RIGHT = 1
MOVE_LEFT = 2
MOVE_UP = 3
MOVE_DOWN = 4



class Enemy(pygame.sprite.Sprite):
    def __init__(self,name,position,level=1):
        super().__init__() 
        self.image = pygame.image.load("sprites/enemy.png")
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.center= position
        self.direction = MOVE_RIGHT
        self.idle_frame_start = time.time()
        self.health = 100
        self.turn_time = time.time()
        self.attack = random.randint(1,100)
        self.defense = random.randint(1,100)
        self.level = level or 1
        self.exp = 20

    def move(self,obstacles):

        up, down, left, right = True, True, True, True
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(self,obstacle):
                if self.rect.top <= obstacle.rect.bottom and self.rect.bottom > obstacle.rect.bottom: # check if top collide
                    up = False
                if self.rect.right >= obstacle.rect.left and self.rect.left < obstacle.rect.left: # check if right collide
                    right = False
                if self.rect.left <= obstacle.rect.right and self.rect.right > obstacle.rect.right: # check if left collide
                    left = False
                if self.rect.bottom >= obstacle.rect.top and self.rect.top < obstacle.rect.top:
                    down = False
                break


        if self.rect.right >= SCREEN_WIDTH or not right:        
            self.direction = MOVE_LEFT
        elif self.rect.left <= 0 or not left:
            self.direction = MOVE_RIGHT
        elif self.rect.bottom >= SCREEN_HEIGHT or not down:        
            self.direction = MOVE_UP
        elif self.rect.top <= 0 or not up:
            self.direction = MOVE_DOWN

        if self.direction == MOVE_RIGHT:
            self.rect.move_ip(5, 0)
        elif self.direction == MOVE_LEFT:
            self.rect.move_ip(-5, 0)
        elif self.direction == MOVE_UP:
            self.rect.move_ip(0, -5)
        elif self.direction == MOVE_DOWN:
            self.rect.move_ip(0, 5)
        
        if time.time() - self.turn_time > 3.0: 
            self.direction = random.randint(1,4)
            self.turn_time = time.time()
        self.animate()

    def animate(self):
        if time.time() - self.idle_frame_start > 0.5:
            self.image = pygame.transform.flip(self.image, True, False)
            self.idle_frame_start = time.time()


 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 

    
class Boss(Enemy):
    def __init__(self,name,position):
        super().__init__(name,position,10) 
        self.image = pygame.image.load("sprites/boss.png")
        self.health = 1000
        self.attack = random.randint(500,1000)
        self.defense = random.randint(500,1000)
