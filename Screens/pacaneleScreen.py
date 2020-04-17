from Screens.screen import Screen, QUIT_PROGRAM
import pygame
import os
import random
from constants import TEXT_FONT, TEXT_FONT_SIZE, NR_PREV_COLORS, BOX_SIZE, PACANELE_FONT, PACANELE_FONT_SIZE, GAP_SIZE,\
    PACANELE_BG_COLOR, DOUBLE_MONEY_BOX_LEFT, DOUBLE_MONEY_BOX_TOP, DOUBLE_MONEY_BOX_WIDTH, HIGHLIGHT_COLOR, HIGHLIGHT_BORDER_SIZE,\
    TEXT_ROW_HEIGHT, WINDOW_WIDTH, LIGHT_BG_COLOR, LIGHT_ORANGE, WINDOW_HEIGHT, PACANELE_FONT_COLOR
from song import Song
from pygame.constants import QUIT, MOUSEMOTION, K_ESCAPE, KEYUP, MOUSEBUTTONUP

ACE_OF_SPADES_IMAGE = "ACE_SPADES.jpg"
ACE_OF_HEARTS_IMAGE = "ACE_HEARTS.jpg"
SAVE_ICON_IMAGE = "SAVE_ICON.jpg"

PACANELE_SONG_PATH = "Music//PACANELE.ogg"

class PacaneleScreen(Screen):
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        
        self.__font = pygame.font.SysFont(TEXT_FONT, TEXT_FONT_SIZE, True, False)
        self.__aceOfSpades = self.__loadSpecialImage(ACE_OF_SPADES_IMAGE)
        self.__aceOfHearts = self.__loadSpecialImage(ACE_OF_HEARTS_IMAGE)
        self.__saveIcon = self.__loadSpecialImage(SAVE_ICON_IMAGE)
        
        self.__lastColors = [-1] * NR_PREV_COLORS
        self.__pacaneleFont = pygame.font.SysFont(PACANELE_FONT, PACANELE_FONT_SIZE, True)
        self.__LEFT_MARGIN = NR_PREV_COLORS * BOX_SIZE + (NR_PREV_COLORS - 1) * GAP_SIZE
        
        self.__previousSongTime = 0
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(PACANELE_BG_COLOR)
    
    def setBackgroundMusic(self):
        self.__previousSongTime = Song(PACANELE_SONG_PATH).play(-1, 0)
        
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
    
    def __displayBox(self):
        pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, (DOUBLE_MONEY_BOX_LEFT, DOUBLE_MONEY_BOX_TOP, DOUBLE_MONEY_BOX_WIDTH, TEXT_ROW_HEIGHT))
        textBlock = self.__font.render("Dubleaza", True, LIGHT_ORANGE)
        textRect = textBlock.get_rect()
        textRect.center = (DOUBLE_MONEY_BOX_LEFT + DOUBLE_MONEY_BOX_WIDTH / 2, DOUBLE_MONEY_BOX_TOP + TEXT_ROW_HEIGHT / 2)
        self.__gameDisplay.blit(textBlock, textRect)
    
    def __displayLastColors(self):
        for i in range(NR_PREV_COLORS):
            if self.__lastColors[i] == 0:
                self.__gameDisplay.blit(self.__aceOfHearts, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT // 4))
            elif self.__lastColors[i] == 1:
                self.__gameDisplay.blit(self.__aceOfSpades, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT // 4))
            else:
                pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + i * (BOX_SIZE + GAP_SIZE), WINDOW_HEIGHT // 4, BOX_SIZE, BOX_SIZE))
    
    def __displayContent(self, money):
        textBlock = self.__font.render("%.2f lei" % money, True, LIGHT_ORANGE)
        textRect = textBlock.get_rect()
        textRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.__gameDisplay.blit(textBlock, textRect)
        
        self.__gameDisplay.blit(self.__aceOfHearts, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2, 3 * WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__aceOfSpades, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + 3 * (BOX_SIZE + GAP_SIZE), 3 * WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__saveIcon, ((WINDOW_WIDTH - self.__LEFT_MARGIN) // 2 + 6 * (BOX_SIZE + GAP_SIZE), 3 * WINDOW_HEIGHT // 4))
    
    def __checkResult(self, choice):
        actualResult = random.randint(0, 1)
        self.__lastColors.insert(0, actualResult)
        self.__lastColors.pop()
        
        return actualResult == choice
    
    def __resultScreen(self, result):
        if result == True:
            textBlock = self.__pacaneleFont.render("WIN", True, PACANELE_FONT_COLOR)
        else:
            textBlock = self.__pacaneleFont.render("LOSS", True, PACANELE_FONT_COLOR)
        textRect = textBlock.get_rect()
        textRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.__gameDisplay.blit(textBlock, textRect)
        
        pygame.display.update()
        pygame.time.wait(1000)
    
    def __redOrBlack(self, money):
        mouseX = mouseY = 0
        choice = -1
        
        while True:
            mouseClicked = False
            
            self.setBackgroundImage()
            self.__displayLastColors()
            self.__displayContent(money)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return QUIT_PROGRAM
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
                    self.__resultScreen(True)
                else:
                    self.__resultScreen(False)
                    return 0.0
    
    def displayContent(self, mouseX, mouseY, mouseClicked, money):
        self.__displayBox()
        
        box = pygame.Rect(DOUBLE_MONEY_BOX_LEFT, DOUBLE_MONEY_BOX_TOP, DOUBLE_MONEY_BOX_WIDTH, TEXT_ROW_HEIGHT)
        if box.collidepoint(mouseX, mouseY):
            pygame.draw.rect(self.__gameDisplay, HIGHLIGHT_COLOR, (DOUBLE_MONEY_BOX_LEFT - HIGHLIGHT_BORDER_SIZE, DOUBLE_MONEY_BOX_TOP - HIGHLIGHT_BORDER_SIZE, DOUBLE_MONEY_BOX_WIDTH + 2 * HIGHLIGHT_BORDER_SIZE, TEXT_ROW_HEIGHT + 2 * HIGHLIGHT_BORDER_SIZE), HIGHLIGHT_BORDER_SIZE)
            if mouseClicked and money > 0.0:
                self.setBackgroundMusic()
                pygame.mouse.set_visible(True)
                
                functionResult = self.__redOrBlack(money)
                if functionResult == QUIT_PROGRAM:
                    return QUIT_PROGRAM
                money = functionResult
                
                self.__playlist.restorePreviousSong(self.__previousSongTime)
                pygame.mouse.set_visible(False)
             
        return money
    
    
    