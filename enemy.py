import pygame, random, time
from settings import *

MOVE_RIGHT = 1
MOVE_LEFT = 2
MOVE_UP = 3
MOVE_DOWN = 4



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("sprites/enemy.png")
        self.name = "Tony Rapon"
        self.rect = self.image.get_rect()
        self.rect.center= (50, 50)
        self.direction = MOVE_RIGHT
        self.idle_frame_start = time.time()
        self.health = 100
        self.turn_time = time.time()
        self.attack = random.randint(1,100)
        self.defense = random.randint(1,100)
        self.level = 1
        self.exp = 20

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
        surface.blit(self.image, self.rect) 