import pygame
from settings import *
from pygame.locals import *

class Dialog(pygame.sprite.Sprite):
    
    def __init__(self, x, y, texts, font=None, name=None):
        super().__init__()
        self.option = 1
        self.font_texts = []
        self.width = 0
        self.height = 0
        self.font = font or pygame.font.Font(FONT_TYPE,FONT_SMALL)
        self.x = x
        self.y = y
        self.name = name
        if self.name:
            texts.insert(0, self.name + ": ")
        for text in texts:
            font_text = self.font.render(text, True, WHITE)
            self.font_texts.append(font_text)
            if font_text.get_width() > self.width:
                self.width = font_text.get_width()
            self.height = self.height + font_text.get_height()
        #self.height = self.height - (font_text.get_height()*2)
        
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, pygame.Rect(self.x - DIALOG_BORDER, self.y -  DIALOG_BORDER, self.width + (DIALOG_BORDER * 2), self.height + (DIALOG_BORDER * 2)))
        pygame.draw.rect(surface, BLACK, pygame.Rect(self.x, self.y, self.width, self.height))
        pos_y = self.y
        for font in self.font_texts:
            surface.blit(font, (self.x,pos_y))
            pos_y = pos_y + font.get_height()
        #pygame.display.flip()
    
    def update_text(self, texts):
        self.font_texts = []
        self.width = 0
        self.height = 0
        if self.name:
            texts.insert(0, self.name + ": ")
        for text in texts:
            font_text = self.font.render(text, True, WHITE)
            self.font_texts.append(font_text)
            if font_text.get_width() > self.width:
                self.width = font_text.get_width()
            self.height = self.height + font_text.get_height()

class Menu(Dialog):
    def __init__(self, x, y, texts):
        super().__init__(x, y, texts, pygame.font.Font(FONT_TYPE,FONT_LARGE))
        self.options = texts

    def draw(self, surface):
        menu_width = self.width + 50
        pygame.draw.rect(surface, WHITE, pygame.Rect(self.x - DIALOG_BORDER, self.y -  DIALOG_BORDER, menu_width +  (DIALOG_BORDER * 2), self.height +  (DIALOG_BORDER * 2)))
        pygame.draw.rect(surface, BLACK, pygame.Rect(self.x, self.y, menu_width, self.height))
        pos_y = self.y
        count = 1
        for font in self.font_texts:
            if count == self.option:
                pygame.draw.rect(surface, WHITE, pygame.Rect(self.x + 10, pos_y + (font.get_height()/2) - 10, 20, 20))
            surface.blit(font, (self.x + 50,pos_y))
            pos_y = pos_y + font.get_height()
            count += 1

    def update(self,events,player):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key==K_UP:
                    if self.option == 1:
                        self.option = len(self.font_texts)
                    else:
                        self.option -= 1
                if event.key==K_DOWN:
                    if self.option == len(self.font_texts):
                        self.option = 1
                    else:
                        self.option += 1
                if event.key==K_SPACE:
                    if player.status == FIGHTING:
                        if self.options[self.option - 1] == ATTACK:
                            player.status = ATTACKING
                        elif self.options[self.option - 1] == MAGIC:
                            player.status = CASTING
                        elif self.options[self.option - 1] == DEFEND:
                            player.status = DEFENDING
                        elif self.options[self.option - 1] == RUN:
                            player.status = RUNNING
                    elif player.status == CASTING:
                        if player.spells[self.option - 1].cost <= player.magic:
                            if player.spells[self.option - 1].name == "Heal":
                                player.health += player.spells[self.option - 1].points
                                player.status = WAITING
                            elif player.spells[self.option - 1].name == "Fireball":
                                player.attack = player.spells[self.option - 1].points
                                player.status = ATTACKING
                            player.magic -= player.spells[self.option - 1].cost
                        else:
                            player.status = FIGHTING
                        self.update_text([ATTACK,MAGIC,DEFEND,RUN])
                    self.option = 1
