import pygame
from constants import *
import random

class DoubleMoney:
    def __init__(self, gameDisplay, font, audioRepo, aceHearts, aceSpades):
        self.__gameDisplay = gameDisplay
        self.__font = font
        self.__audioRepo = audioRepo
        self.__aceHearts = aceHearts
        self.__aceSpades = aceSpades
        
        #0 = red, 1 = black
        self.__lastColors = [-1] * NR_PREV_COLORS
    
    def __displayBox(self):
        pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, (DOUBLE_MONEY_BOX_LEFT, DOUBLE_MONEY_BOX_TOP, DOUBLE_MONEY_BOX_WIDTH, TEXT_ROW_HEIGHT))
        self.__gameDisplay.blit(self.__font.render("Dubleaza", True, LIGHT_ORANGE, None), (DOUBLE_MONEY_BOX_LEFT + 13, DOUBLE_MONEY_BOX_TOP + 10))
    
    def __displayLastColors(self):
        x = 7 * BOX_SIZE + 6 * GAP_SIZE
        for i in range(NR_PREV_COLORS):
            if self.__lastColors[i] == 0:
                self.__gameDisplay.blit(self.__aceHearts, ((WINDOW_WIDTH - x) / 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT / 4))
            elif self.__lastColors[i] == 1:
                self.__gameDisplay.blit(self.__aceSpades, ((WINDOW_WIDTH - x) / 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT / 4))
            else:
                pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, ((WINDOW_WIDTH - x) / 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT / 4, BOX_SIZE, BOX_SIZE))
    
    def __displayContent(self, money):
        self.__gameDisplay.blit(self.__font.render("%.2f lei" % money, True, LIGHT_ORANGE, None), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2))
        self.__gameDisplay.blit(self.__aceHearts, )
        self.__gameDisplay.blit(self.__aceSpades, )
        pygame
        #display 3 buttons - red, black, cash out
    
    def __redOrBlack(self, money):
        prevSongTime = self.__audioRepo.playPacaneleSong()
        while True:
            self.__gameDisplay.fill(BG_COLOR)
            self.__displayLastColors()
            self.__displayContent(money)
            pygame.display.update()
    
        self.__audioRepo.endPacaneleSong(prevSongTime)
    
    def doubleMoney(self, mouseX, mouseY, mouseClicked, money):
        self.__displayBox()
        
        box = pygame.Rect(DOUBLE_MONEY_BOX_LEFT, DOUBLE_MONEY_BOX_TOP, DOUBLE_MONEY_BOX_WIDTH, TEXT_ROW_HEIGHT)
        if box.collidepoint(mouseX, mouseY):
            pygame.draw.rect(self.__gameDisplay, HIGHLIGHT_COLOR, (DOUBLE_MONEY_BOX_LEFT - HIGHLIGHT_BORDER_SIZE, DOUBLE_MONEY_BOX_TOP - HIGHLIGHT_BORDER_SIZE, DOUBLE_MONEY_BOX_WIDTH + 2 * HIGHLIGHT_BORDER_SIZE, TEXT_ROW_HEIGHT + 2 * HIGHLIGHT_BORDER_SIZE), HIGHLIGHT_BORDER_SIZE)
            if mouseClicked:
                self.__redOrBlack(money)
        else:
            return