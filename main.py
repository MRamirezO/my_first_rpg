import sys, pygame
from settings import *
from player import *
from background import *
from enemy import *
from pygame import mixer
from scenes import *
from maps import *

FramePerSec = pygame.time.Clock()
size = SCREEN_WIDTH, SCREEN_HEIGHT

screen = pygame.display.set_mode(size)

mixer.init()

P1 = Player()

battle_scene = None

village_scene = None

world_scene = WorldMap(P1, WORLD_MAP)

current_scene = world_scene

game_status = WORLD_MAP

while True:
    events = pygame.event.get()
    for event in events:   
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if game_status == WORLD_MAP:
        for door in current_scene.doors:
            if pygame.sprite.collide_rect(P1, door):
                del(world_scene)
                P1.rect.topleft = (100, 100)
                if door.destination == VILLAGE:
                    game_status = TOWN
                    village_scene = Village(P1,INITIAL_VILLAGE)
                    current_scene = village_scene
                elif door.destination == CAVE:
                    game_status = DUNGEON
                    village_scene = Dungeon(P1,DUNGEON_MAP)
                    current_scene = village_scene
                elif door.destination == CASTLE:
                    game_status = TOWN
                    village_scene = Castle(P1,CASTLE_MAP)
                    current_scene = village_scene
        for enemy in current_scene.enemies:
            if pygame.sprite.collide_rect(P1, enemy):
                game_status = BATTLE
                P1.status = FIGHTING
                del(world_scene)
                battle_scene = BattleScene(P1,enemy)
                current_scene = battle_scene
                current_scene.enemy.rect.center = (600, 520)
                break
                
    elif game_status == DUNGEON:
        if P1.rect.top <= 0 or P1.rect.bottom >= SCREEN_HEIGHT or P1.rect.left <= 0 or P1.rect.right >= SCREEN_WIDTH:
            game_status = WORLD_MAP
            P1.status = EXPLORING
            P1.rect.topleft = (100, 400)
            del(village_scene)
            world_scene = WorldMap(P1, WORLD_MAP)
            current_scene = world_scene
        else:
            for enemy in current_scene.enemies:
                if pygame.sprite.collide_rect(P1, enemy):
                    game_status = BATTLE
                    P1.status = FIGHTING
                    del(village_scene)
                    battle_scene = BattleScene(P1,enemy)
                    current_scene = battle_scene
                    current_scene.enemy.rect.center = (600, 520)
                    break

    elif game_status == TOWN:
        if P1.rect.top <= 0 or P1.rect.bottom >= SCREEN_HEIGHT or P1.rect.left <= 0 or P1.rect.right >= SCREEN_WIDTH:
            game_status = WORLD_MAP
            P1.status = EXPLORING
            P1.rect.topleft = (100, 400)
            del(village_scene)
            world_scene = WorldMap(P1, WORLD_MAP)
            current_scene = world_scene     
            
    elif game_status == BATTLE:
        if P1.health <= 0:
            game_status = GAME_OVER
            pygame.quit()
            sys.exit()
        elif current_scene.enemy.health <= 0:
            if P1.status is not RUNNING:
                P1.get_experience(current_scene.enemy)
            game_status = WORLD_MAP
            P1.status = EXPLORING
            del(battle_scene)
            world_scene = WorldMap(P1, WORLD_MAP)
            current_scene = world_scene
     
    current_scene.update(events)           
    current_scene.draw(screen)
        
    pygame.display.update()
    FramePerSec.tick(FPS)