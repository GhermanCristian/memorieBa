from Screens.screen import Screen
import pygame
import os
import random
from constants import Constants
from song import Song
from text import Text
from label import Label
from button import Button
from pygame.constants import QUIT, MOUSEMOTION, K_ESCAPE, KEYUP, MOUSEBUTTONUP

class PacaneleScreen(Screen):
    ACE_OF_SPADES_IMAGE = "ACE_SPADES.jpg"
    ACE_OF_HEARTS_IMAGE = "ACE_HEARTS.jpg"
    SAVE_ICON_IMAGE = "SAVE_ICON.jpg"
    
    SONG_PATH = "Music//PACANELE.ogg"

    BOX_SIZE = 130
    GAP_SIZE = 10
    NR_PREV_COLORS = 7
    PREVIOUS_RESULTS_LEFT_MARGIN = (Constants.WINDOW_WIDTH - NR_PREV_COLORS * BOX_SIZE - (NR_PREV_COLORS - 1) * GAP_SIZE) // 2
    
    TEXT_FONT = "felixtitling"
    TEXT_FONT_SIZE = 256
    TEXT_FONT_COLOR = Constants.GOLD
    
    MONEY_TEXT_FONT = "lucidasans"
    MONEY_TEXT_FONT_SIZE = 20
    MONEY_TEXT_COLOR = Constants.LIGHT_ORANGE
    MONEY_TEXT_ROW_HEIGHT = 50
    
    BG_COLOR = Constants.NAVY_RED
    LIGHT_BG_COLOR = Constants.GRAY
    
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        
        self.__font = pygame.font.SysFont(PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.TEXT_FONT_SIZE, True, False)
        self.__aceOfSpades = self.__loadSpecialImage(PacaneleScreen.ACE_OF_SPADES_IMAGE)
        self.__aceOfHearts = self.__loadSpecialImage(PacaneleScreen.ACE_OF_HEARTS_IMAGE)
        self.__saveIcon = self.__loadSpecialImage(PacaneleScreen.SAVE_ICON_IMAGE)
        
        self.__lastColors = [-1] * PacaneleScreen.NR_PREV_COLORS
        self.__pacaneleFont = pygame.font.SysFont(PacaneleScreen.TEXT_FONT, PacaneleScreen.TEXT_FONT_SIZE, True)
        
        self.__previousSongTime = 0
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(PacaneleScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        self.__previousSongTime = Song(PacaneleScreen.SONG_PATH).play(-1, 0)
        
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
    
    def __displayLastColors(self):
        for i in range(PacaneleScreen.NR_PREV_COLORS):
            if self.__lastColors[i] == 0:
                self.__gameDisplay.blit(self.__aceOfHearts, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN+ i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), Constants.WINDOW_HEIGHT // 4))
            elif self.__lastColors[i] == 1:
                self.__gameDisplay.blit(self.__aceOfSpades, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), Constants.WINDOW_HEIGHT // 4))
            else:
                pygame.draw.rect(self.__gameDisplay, PacaneleScreen.LIGHT_BG_COLOR, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE))
    
    def __displayContent(self, money):        
        moneyText = Text("%.2f lei" % money, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR)
        Label(Constants.WINDOW_HEIGHT / 2 - PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, Constants.WINDOW_WIDTH / 2 - len(moneyText.content) * PacaneleScreen.MONEY_TEXT_FONT_SIZE / 2, -1, PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, PacaneleScreen.BG_COLOR, moneyText).display(self.__gameDisplay)
        
        self.__gameDisplay.blit(self.__aceOfHearts, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__aceOfSpades, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__saveIcon, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 6 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4))
    
    def __checkResult(self, choice):
        actualResult = random.randint(0, 1)
        self.__lastColors.insert(0, actualResult)
        self.__lastColors.pop()
        
        return actualResult == choice
    
    def __resultScreen(self, result):
        if result == True:
            textBlock = self.__pacaneleFont.render("WIN", True, PacaneleScreen.TEXT_FONT_COLOR)
        else:
            textBlock = self.__pacaneleFont.render("LOSS", True, PacaneleScreen.TEXT_FONT_COLOR)
        textRect = textBlock.get_rect()
        textRect.center = (Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT / 2)
        self.__gameDisplay.blit(textBlock, textRect)
        
        pygame.display.update()
        pygame.time.wait(1000)
    
    def __redOrBlack(self, money):
        mouseX = mouseY = 0
        choice = -1
        
        redBox = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        blackBox = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        saveBox = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 6 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        
        while True:
            mouseClicked = False
            
            self.setBackgroundImage()
            self.__displayLastColors()
            self.__displayContent(money)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return money
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    mouseClicked = True
                    
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
    
    def displayContent(self, money):
        self.setBackgroundMusic()
        pygame.mouse.set_visible(True)
        
        functionResult = self.__redOrBlack(money)
        
        self.__playlist.restorePreviousSong(self.__previousSongTime)
        pygame.mouse.set_visible(False)

        money = functionResult             
        return money
    
    
    