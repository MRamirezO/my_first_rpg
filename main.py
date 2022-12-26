import sys, pygame
from settings import *
from player import *
from background import *
from enemy import *
from pygame import mixer
from scenes import *

FramePerSec = pygame.time.Clock()
size = SCREEN_WIDTH, SCREEN_HEIGHT

screen = pygame.display.set_mode(size)

mixer.init()
enemy_hit = mixer.Sound("sfx/die.wav")

P1 = Player()

battle_scene = None

world_scene = WorldMap(P1)

current_scene = world_scene

game_status = WORLD_MAP

while True:
    events = pygame.event.get()
    for event in events:   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if game_status not in (BATTLE, STORY, MENU):
        if pygame.sprite.collide_rect(P1, current_scene.E1):
            game_status = BATTLE
            P1.status = FIGHTING
            mixer.music.stop()
            del(world_scene)
            battle_scene = BattleScene(P1,current_scene.E1)
            current_scene = battle_scene
            current_scene.enemy.rect.center = (600, 520)

            
    if game_status == BATTLE:
        if P1.health <= 0:
            game_status = GAME_OVER
            pygame.quit()
            sys.exit()
        elif current_scene.enemy.health <= 0:
            P1.get_experience(current_scene.enemy)
            game_status = WORLD_MAP
            P1.status = EXPLORING
            del(battle_scene)
            world_scene = WorldMap(P1)
            current_scene = world_scene
     
    current_scene.update(events)           
    current_scene.draw(screen)
        
    pygame.display.update()
    FramePerSec.tick(FPS)