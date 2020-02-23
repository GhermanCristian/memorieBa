import pygame
from constants import *
import random
from pygame.constants import *

class DoubleMoney:
    def __init__(self, gameDisplay, font, audioRepo, aceHearts, aceSpades, saveIcon):
        self.__gameDisplay = gameDisplay
        self.__font = font
        self.__audioRepo = audioRepo
        self.__aceHearts = aceHearts
        self.__aceSpades = aceSpades
        self.__saveIcon = saveIcon
        
        #0 = red, 1 = black; the most recent element is the first one
        self.__lastColors = [-1] * NR_PREV_COLORS
        
        self.__LEFT_MARGIN = NR_PREV_COLORS * BOX_SIZE + (NR_PREV_COLORS - 1) * GAP_SIZE
    
    def __displayBox(self):
        pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, (DOUBLE_MONEY_BOX_LEFT, DOUBLE_MONEY_BOX_TOP, DOUBLE_MONEY_BOX_WIDTH, TEXT_ROW_HEIGHT))
        self.__gameDisplay.blit(self.__font.render("Dubleaza", True, LIGHT_ORANGE, None), (DOUBLE_MONEY_BOX_LEFT + 13, DOUBLE_MONEY_BOX_TOP + 10))
    
    def __displayLastColors(self):
        for i in range(NR_PREV_COLORS):
            if self.__lastColors[i] == 0:
                self.__gameDisplay.blit(self.__aceHearts, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT // 4))
            elif self.__lastColors[i] == 1:
                self.__gameDisplay.blit(self.__aceSpades, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT // 4))
            else:
                pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT // 4, BOX_SIZE, BOX_SIZE))
    
    def __displayContent(self, money):
        self.__gameDisplay.blit(self.__font.render("%.2f lei" % money, True, LIGHT_ORANGE, None), (WINDOW_WIDTH // 2 - 8 * 7, WINDOW_HEIGHT // 2))
        self.__gameDisplay.blit(self.__aceHearts, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2, 3 * WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__aceSpades, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + 3 * (BOX_SIZE + GAP_SIZE), 3 * WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__saveIcon, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + 6 * (BOX_SIZE + GAP_SIZE), 3 * WINDOW_HEIGHT // 4))
    
    def __checkResult(self, choice):
        actualResult = random.randint(0, 1)
        self.__lastColors.insert(0, actualResult)
        self.__lastColors.pop()
        
        return actualResult == choice
    
    def __redOrBlack(self, money):
        mouseX = mouseY = 0
        choice = -1
        
        while True:
            mouseClicked = False
            
            self.__gameDisplay.fill(PACANELE_BG_COLOR)
            self.__displayLastColors()
            self.__displayContent(money)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    mouseClicked = True
                    
            redBox = pygame.Rect((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2, 3 * WINDOW_HEIGHT // 4, BOX_SIZE, BOX_SIZE)
            blackBox = pygame.Rect((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + 3 * (BOX_SIZE + GAP_SIZE), 3 * WINDOW_HEIGHT // 4, BOX_SIZE, BOX_SIZE)
            saveBox = pygame.Rect((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + 6 * (BOX_SIZE + GAP_SIZE), 3 * WINDOW_HEIGHT // 4, BOX_SIZE, BOX_SIZE)
            if mouseClicked == True:
                if redBox.collidepoint(mouseX, mouseY):
                    choice = 0
                elif blackBox.collidepoint(mouseX, mouseY):
                    choice = 1
                elif saveBox.collidepoint(mouseX, mouseY):
                    return money
                else:
                    continue
                
                if self.__checkResult(choice):
                    money *= 2.0
                else:
                    return 0.0
    
    def double(self, mouseX, mouseY, mouseClicked, money):
        self.__displayBox()
        
        box = pygame.Rect(DOUBLE_MONEY_BOX_LEFT, DOUBLE_MONEY_BOX_TOP, DOUBLE_MONEY_BOX_WIDTH, TEXT_ROW_HEIGHT)
        if box.collidepoint(mouseX, mouseY):
            pygame.draw.rect(self.__gameDisplay, HIGHLIGHT_COLOR, (DOUBLE_MONEY_BOX_LEFT - HIGHLIGHT_BORDER_SIZE, DOUBLE_MONEY_BOX_TOP - HIGHLIGHT_BORDER_SIZE, DOUBLE_MONEY_BOX_WIDTH + 2 * HIGHLIGHT_BORDER_SIZE, TEXT_ROW_HEIGHT + 2 * HIGHLIGHT_BORDER_SIZE), HIGHLIGHT_BORDER_SIZE)
            if mouseClicked and money > 0.0:
                prevSongTime = self.__audioRepo.playPacaneleSong()
                pygame.mouse.set_visible(True)
                
                money = self.__redOrBlack(money)
                
                self.__audioRepo.endPacaneleSong(prevSongTime)
                pygame.mouse.set_visible(False)
             
        return money
    
    
    