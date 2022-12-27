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
        mixer.music.load('assets/music/village.mp3')
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
        mixer.music.load('assets/music/castle.mp3')
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
        mixer.music.load('assets/music/dungeon.mp3')
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
        mixer.music.load('assets/music/map_theme.mp3')
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
        mixer.music.load('assets/music/battle_theme.mp3')
        mixer.music.play(-1)
        self.dialog = Dialog(400,60,[f"A wild {self.enemy.name} appeared!"])
        self.actions = Menu(60,500,[ATTACK,MAGIC,DEFEND,RUN])
        self.info = Dialog(1000,600,[f"Level: {self.player.level}",f"HP: {self.player.health}",f"MP: {self.player.magic}"])
        self.enemy_info = Dialog(900,10,[f"Enemy HP: {self.enemy.health}"])
        self.stages = [CHOOSE,ANNOUNCE,PERFORM,RESULT]
        self.stage = 1
        self.delay = 3000   
        self.hit_points = 0 
        self.runaway = 0



    def draw(self, screen):
        screen.fill(pygame.Color('lightblue'))
        self.dialog.draw(screen)
        self.actions.draw(screen)
        self.info.draw(screen)
        self.enemy_info.draw(screen)
        self.enemy.draw(screen)

    def update(self,event):
        if self.player.thinking:
            self.stage = 0
        if self.player.status == FIGHTING:
            self.dialog.update_text(["Choose an action..."])
            self.actions.update(event,self.player)
        elif self.player.status == ATTACKING:
            if self.stages[self.stage] == ANNOUNCE:
                self.dialog.update_text(["Player is attacking!"])
                self.hit_points = random.randint(1,self.player.attack) * self.player.level
            elif self.stages[self.stage] == PERFORM:
                self.dialog.update_text([f"Enemy hit by {self.hit_points}!"])
            elif self.stages[self.stage] == RESULT:
                self.enemy.health -= self.hit_points
                self.enemy_info.update_text([f"Enemy HP: {self.enemy.health}"])
                self.player.attack = 20
                self.player.status = WAITING
                self.stage = 1
        elif self.player.status == CASTING:
            if self.stages[self.stage] == CHOOSE:
                self.dialog.update_text(["Player is casting some magic!"])
                self.actions.update_text([spell.name for spell in self.player.spells])
                self.actions.update(event,self.player)
                if not self.player.thinking:
                    self.stage = 1
            elif self.stages[self.stage] == ANNOUNCE:
                self.dialog.update_text([f"Player casts {self.player.spells[self.actions.option - 1].name}"])
                self.hit_points = self.player.spells[self.actions.option - 1].points
            elif self.stages[self.stage] == PERFORM:
                if self.hit_points > 0:
                    self.dialog.update_text([f"Player healed by {self.hit_points} points"])
                else:
                    self.dialog.update_text([f"Enemy damaged by {self.hit_points} points!"])
            elif self.stages[self.stage] == RESULT:
                self.player.magic -= self.player.spells[self.actions.option - 1].cost
                if self.hit_points > 0:
                    self.player.health += self.hit_points
                else:
                    self.enemy.health += self.hit_points
                self.enemy_info.update_text([f"Enemy HP: {self.enemy.health}"])
                self.info.update_text([f"Level: {self.player.level}",f"HP: {self.player.health}",f"MP: {self.player.magic}"])
                self.actions.update_text([ATTACK,MAGIC,DEFEND,RUN])
                self.stage = 1
                self.player.status = WAITING
            # self.player.status = WAITING
        elif self.player.status == RUNNING:
            if self.stages[self.stage] == ANNOUNCE:
                self.dialog.update_text(["Player is trying to run from enemy!"])
                self.runaway = random.randint(0,1)
            elif self.stages[self.stage] == PERFORM:
                if self.runaway:
                    self.dialog.update_text([f"Player ran away safely!"])
                else:
                    self.dialog.update_text([f"Player can't run away from enemy!"])
            elif self.stages[self.stage] == RESULT:
                if self.runaway:
                    self.enemy.health = 0
                    self.stage = 1
                else:
                    self.player.status = WAITING
                    self.stage = 1
        elif self.player.status == WAITING or self.player.status == DEFENDING:
            if self.stages[self.stage] == ANNOUNCE:
                self.dialog.update_text(["Enemy is attacking!"])
                if self.player.status == DEFENDING:
                    self.hit_points = random.randint(1,5) * self.enemy.level
                else:
                    self.hit_points = random.randint(1,20) * self.enemy.level
            elif self.stages[self.stage] == PERFORM:
                self.dialog.update_text([f"Player hit by {self.hit_points}!"])
            elif self.stages[self.stage] == RESULT:
                self.player.health -= self.hit_points
                self.info.update_text([f"Level: {self.player.level}",f"HP: {self.player.health}",f"MP: {self.player.magic}"])
                self.actions.option = 1
                self.player.status = FIGHTING
                self.stage = 1
            

        if self.player.status is not FIGHTING and self.stage != 0:
            now = pygame.time.get_ticks()
            if now - self.player.last_action >= self.delay:
                self.player.last_action = now
                if self.stage == len(self.stages) - 1:
                    self.stage = 1
                else:
                    self.stage += 1

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