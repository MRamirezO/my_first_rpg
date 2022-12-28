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
BEGINNING = "BEGINNING"
EXPLORING = "EXPLORING"
TALKING = "TALKING"
SLEEPING = "SLEEPING"
FIGHTING = "FIGHTING"
ATTACKING = "ATTACKING"
CASTING = "CASTING"
DEFENDING = "DEFENDING"
RUNNING = "RUNNING"
WAITING = "WAITING"

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
TILE_SIZE = 96

#Setting up Fonts
FONT_TYPE = "assets/fonts/eightbitmadness.ttf"
FONT_SMALL = 60
FONT_LARGE = 90
FONT_MEDIUM = 70

# Attributes
HEALTH = "Health"
MAGIC = "Magic"
DEFENSE = "Defense"
SPEED = "Speed"
ACCURACY = "Accuracy"

# Battle stages
CHOOSE = "CHOOSE"
ANNOUNCE = "ANNOUNCE"
PERFORM = "PERFORM"
RESULT = "RESULT"