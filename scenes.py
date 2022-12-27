import pygame, random, itertools
from background import *
from pygame import mixer
from settings import *
from misc import *
from enemy import *
from npc import *
from tiles import *

class Map:
    
    def __init__(self, tile_map):
        self.tileset = []
        self.obstacles = []
        self.doors = []
        self.enemies = []
        x,y = 0, 0
        for tile_row in tile_map:
            row = []
            for tile_type in tile_row:
                if tile_type in (GROUND,GREEN_GRASS,WOODEN_FLOOR,CARPET):
                    row.append(Tile(tile_type,x,y))
                elif tile_type in (WALL,WATER,CASTLE_WALL):
                    obstacle = Obstacle(tile_type,x,y)
                    self.obstacles.append(obstacle)
                    row.append(Obstacle(tile_type,x,y))
                elif tile_type in (LAVA,POISON):
                    row.append(Trap(tile_type,x,y))
                elif tile_type in (VILLAGE,CAVE,CASTLE):
                    dest = Portal(tile_type,x,y,tile_type)
                    self.doors.append(dest)
                    row.append(dest)
                x += TILE_SIZE
            y += TILE_SIZE
            x=0
            self.tileset.append(row)

    def draw(self,screen):
        for tile_row in self.tileset:
            for tile in tile_row:
                tile.draw(screen)

class Village(Map):
    npc_list = []
    def __init__(self, player, tile_map):
        super().__init__(tile_map) 
        self.npc_list.append(
            NPC(
                "Layo",
                (900,0),
                ["Hello there!","Soy Mexicano!"]
            )
        )
        self.npc_list.append(
            NPC(
                "Tony",
                (500,600),
                ["Hey guys...","Where's Mica?", "Aaaaa noooo!"]
            )
        )
        self.player = player
        mixer.music.stop()
        mixer.music.load('music/village.mp3')
        mixer.music.play(-1)

    def draw(self, screen):
        super().draw(screen)
        for npc in self.npc_list:
            npc.draw(screen)
            if npc.dialog:
                npc.dialog.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        self.player.draw(screen)
            

    def update(self,events):

        if self.player.status == EXPLORING:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key==K_SPACE:
                        for npc in self.npc_list:
                            if pygame.sprite.collide_rect(self.player, npc):
                                npc.dialog = Dialog(500,60,[npc.dialogs[npc.dialog_index - 1]],name=npc.name)
                                self.player.status = TALKING
                                self.player.talking_to = npc
                                break
                        
            self.player.update(self.obstacles)
            for enemy in self.enemies:
                enemy.move(self.obstacles)
            
        elif self.player.status == TALKING:
            self.player.talking_to.talk(events)
            if not self.player.talking_to.dialog:
                self.player.talking_to = None
                self.player.status = EXPLORING

class Castle(Village):
    def __init__(self, player, tile_map):
        super().__init__(player,tile_map) 
        self.npc_list = []
        self.npc_list.append(
            NPC(
                "King",
                (900,100),
                ["Hello there", "The monsters kidnapped the princess...","Please save my daughter!"]
            )
        )
        self.player = player
        mixer.music.stop()
        mixer.music.load('music/castle.mp3')
        mixer.music.play(-1)

class Dungeon(Village):
    def __init__(self, player, tile_map):
        super().__init__(player,tile_map) 
        self.npc_list = []
        self.enemies.append(
            Enemy(
                "Minion",
                (500,500),
            )
        )
        self.enemies.append(
            Enemy(
                "Minion",
                (600,500),
            )
        )
        self.enemies.append(
            Boss(
                "El chilo",
                (1000,500),
            )
        )
        self.player = player
        mixer.music.stop()
        mixer.music.load('music/dungeon.mp3')
        mixer.music.play(-1)

class WorldMap(Map):
    def __init__(self, player, tile_map):
        super().__init__(tile_map) 
        self.enemies.append(
            Enemy(
                "Minion",
                (200,100),
            )
        )
        self.player = player
        mixer.music.load('music/map_theme.mp3')
        mixer.music.play(-1)

    def draw(self, screen):
        super().draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        self.player.draw(screen)

    def update(self,events):

        if self.player.status == EXPLORING:                        
            self.player.update(self.obstacles)
            for enemy in self.enemies:
                enemy.move(self.obstacles)
            
            
        # self.clouds.update(dt, events)

class BattleScene:
    def __init__(self, player, enemy):
        self.enemy = enemy
        self.player = player
        mixer.music.stop()
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