import pygame, time
from pygame.locals import *
from settings import *
from magic import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("sprites/player_idle.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 520)
        self.idle_frame_start = time.time()
        self.spells = [Spell("Fireball",HEALTH,50,8),Spell("Heal",HEALTH,20,5)]
        self.direction = "down"
        self.health = 100
        self.magic = 100
        self.level = 1
        self.attack = 20
        self.defense = 50
        self.walk_frame = 1
        self.next_level = 10
        self.exp = 0
        self.talking_to = None
        self.status = EXPLORING
 
    def update(self, obstacles):
        up, down, left, right = True, True, True, True
        pressed_keys = pygame.key.get_pressed()
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(self,obstacle):
                if self.rect.top <= obstacle.rect.bottom and self.rect.bottom > obstacle.rect.bottom: # check if top collide
                    up = False
                    #self.rect.top = obstacle.rect.bottom + 5
                if self.rect.right >= obstacle.rect.left and self.rect.left < obstacle.rect.left: # check if right collide
                    right = False
                    #self.rect.right = obstacle.rect.left - 5
                if self.rect.left <= obstacle.rect.right and self.rect.right > obstacle.rect.right: # check if left collide
                    left = False
                    #self.rect.left = obstacle.rect.right + 5
                if self.rect.bottom >= obstacle.rect.top and self.rect.top < obstacle.rect.top:
                    down = False
                    #self.rect.bottom = obstacle.rect.top - 5
                break

        if self.rect.top > 0 and up:
            if pressed_keys[K_UP]:
                    if self.direction != "up":
                        self.direction = "up"
                        self.image = pygame.image.load("sprites/player_back.png")
                    self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT and down:
            if pressed_keys[K_DOWN]:
                    if self.direction != "down":
                        self.direction = "down"
                        self.image = pygame.image.load("sprites/player_idle.png")
                    self.rect.move_ip(0,5)
         
        if self.rect.left > 0 and left:
            if pressed_keys[K_LEFT]:
                if self.direction != "left":
                    self.direction = "left"
                    self.image = pygame.image.load("sprites/player_side_1.png")
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and right:        
            if pressed_keys[K_RIGHT]:
                if self.direction != "right":
                    self.direction = "right"
                    self.image = pygame.transform.flip(pygame.image.load("sprites/player_side_1.png"), True, False)
                self.rect.move_ip(5, 0)
        self.animate()
        

    def animate(self):
        if time.time() - self.idle_frame_start > 0.5:
            if self.direction in ("down","up"):
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.direction == "left":
                self.image = pygame.image.load(f"sprites/player_side_{self.walk_frame}.png")
            elif self.direction == "right":
                self.image = pygame.transform.flip(pygame.image.load(f"sprites/player_side_{self.walk_frame}.png"), True, False)
            if self.walk_frame == 1:
                self.walk_frame = 2
            else:
                self.walk_frame = 1
            self.idle_frame_start = time.time()
        
    def get_experience(self, enemy):
        earned = enemy.exp

        while True:
            left = self.next_level - self.exp
            if earned >= left:
                self.level += 1
                self.next_level = self.next_level * 2
                earned -= left
                self.exp = 0
            else:
                self.exp += earned
                break

 
    def draw(self, surface):
        surface.blit(self.image, self.rect)  