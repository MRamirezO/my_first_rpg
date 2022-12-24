import pygame

pygame.init()

FPS = 60

# Dialog settings
DIALOG_BORDER = 5

# Game status
WORLD_MAP = "WORLD_MAP"
TOWN = "TOWN"
DUNGEON = "DUNGEON"
BATTLE = "BATTLE"
MENU = "MENU"
STORY = "STORY"
GAME_OVER = "GAME_OVER"

# Player status
EXPLORING = "EXPLORING"
TALKING = "TALKING"
SLEEPING = "SLEEPING"
FIGHTING = "FIGHTING"
ATTACKING = "ATTACKING"
CASTING = "CASTING"
DEFENDING = "DEFENDING"
RUNNING = "RUNNING"

# Menu options
NEW_GAME = "New game"
CONTINUE = "Continue"

# Battle Options
ATTACK = "Attack"
MAGIC = "Magic"
DEFEND = "Defend"
RUN = "Run"

# Chat options
SAY_YES = "Yes"
SAY_NO = "No"
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Setting up Fonts
FONT_TYPE = "Verdana"
FONT_SMALL = 25
FONT_LARGE = 55
FONT_MEDIUM = 40