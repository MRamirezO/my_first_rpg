import pygame, random, itertools
from background import *
from pygame import mixer
from settings import *
from misc import *
from enemy import *
from npc import *

class Map:
    pass

class WorldMap:
    def __init__(self, player):
        self.E1 = Enemy()
        self.NPC = NPC()
        self.background = Background('sprites/bg_grass.png', [0,0])
        self.player = player
        mixer.music.load('music/map_theme.mp3')
        mixer.music.play(-1)

    def draw(self, screen):
        self.background.draw(screen)
        self.E1.draw(screen)
        self.NPC.draw(screen)
        self.player.draw(screen)
        if self.NPC.dialog:
            self.NPC.dialog.draw(screen)

    def update(self,events):
        
        if self.player.status == EXPLORING:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key==K_SPACE:
                        if pygame.sprite.collide_rect(self.player, self.NPC):
                            self.NPC.dialog = Dialog(500,60,[self.NPC.dialogs[self.NPC.dialog_index - 1]],name=self.NPC.name)
                            self.player.status = TALKING
            self.player.update()
            self.E1.move()

        elif self.player.status == TALKING:
            self.NPC.talk(events)
            if not self.NPC.dialog:
                self.player.status = EXPLORING
            
        # self.clouds.update(dt, events)

class BattleScene:
    def __init__(self, player, enemy):
        self.enemy = enemy
        self.player = player
        #self.background = Background('sprites/malecon.png', [0,0])
        mixer.music.load('music/battle_theme.mp3')
        mixer.music.play(-1)
        self.dialog = Dialog(500,60,[f"A wild {self.enemy.name} appeared!"])
        self.actions = Menu(60,400,[ATTACK,MAGIC,DEFEND,RUN])
        self.info = Dialog(1100,600,[f"Level: {self.player.level}",f"HP: {self.player.health}",f"MP: {self.player.magic}"])
        self.enemy_info = Dialog(1000,10,[f"Enemy HP: {self.enemy.health}"])



    def draw(self, screen):
        screen.fill(pygame.Color('lightblue'))
        self.dialog.draw(screen)
        self.actions.draw(screen)
        self.info.draw(screen)
        self.enemy_info.draw(screen)
        self.enemy.draw(screen)

    def update(self,event):
        self.actions.update(event,self.player)
        if self.player.status == FIGHTING:
            self.dialog.update_text(["Choose an action..."])
        elif self.player.status == ATTACKING:
            self.dialog.update_text(["Player is attacking!"])
            hit_points = random.randint(1,self.player.attack) * self.player.level
            self.dialog.update_text([f"Enemy hit by {hit_points}!"])
            self.enemy.health -= hit_points
            self.enemy_info.update_text([f"Enemy HP: {self.enemy.health}"])
            self.player.attack = 20
            self.player.status = WAITING
        elif self.player.status == CASTING:
            self.dialog.update_text(["Player is casting some magic!"])

            self.actions.update_text([spell.name for spell in self.player.spells])

            # hit_points = random.randint(1,40)
            # self.dialog.update_text([f"Enemy hit by {hit_points}!"])
            # self.player.magic -= 5
            # self.enemy.health -= hit_points
            # self.enemy_info.update_text([f"Enemy HP: {self.enemy.health}"])
            self.info.update_text([f"Level: {self.player.level}",f"HP: {self.player.health}",f"MP: {self.player.magic}"])
            # self.player.status = WAITING
        elif self.player.status == DEFENDING:
            self.dialog.update_text(["Player is defending!"])
            self.dialog.update_text(["Enemy is attacking!"])
            hit_points = random.randint(1,5) * self.player.level
            self.dialog.update_text([f"Player hit by {hit_points}!"])
            self.player.health -= hit_points
            self.info.update_text([f"Level: {self.player.level}",f"HP: {self.player.health}",f"MP: {self.player.magic}"])
            self.player.status = FIGHTING
        elif self.player.status == RUNNING:
            self.dialog.update_text(["Player is trying to run from enemy!"])
            self.enemy.health = 0
        elif self.player.status == WAITING:
            self.dialog.update_text(["Enemy is attacking!"])
            hit_points = random.randint(1,20) * self.enemy.level
            self.dialog.update_text([f"Player hit by {hit_points}!"])
            self.player.health -= hit_points
            self.info.update_text([f"Level: {self.player.level}",f"HP: {self.player.health}",f"MP: {self.player.magic}"])
            self.player.status = FIGHTING

class Fader:

    def __init__(self, scenes):
        self.scenes = itertools.cycle(scenes)
        self.scene = next(self.scenes)
        self.fading = None
        self.alpha = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)
        self.veil.fill((0, 0, 0))

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self, screen):
        self.scene.draw(screen)
        if self.fading:
            self.veil.set_alpha(self.alpha)
            screen.blit(self.veil, (0, 0))

    def update(self, dt, events):
        self.scene.update(dt, events)

        if self.fading == 'OUT':
            self.alpha += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                self.scene = next(self.scenes)
        else:
            self.alpha -= 8
            if self.alpha <= 0:
                self.fading = None