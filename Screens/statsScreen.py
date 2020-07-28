from Screens.screen import Screen
import pygame
from constants import Constants
from pygame.constants import QUIT, KEYUP, K_ESCAPE, K_RIGHT, MOUSEMOTION, MOUSEBUTTONUP
from text import Text

class StatsScreen(Screen):
    TEXT_FONT = "candara"
    TEXT_FONT_SIZE = 30
    TEXT_FONT_CHARACTER_WIDTH = 30
    TEXT_COLOR = Constants.PALE_GOLD
    TEXT_LEFT_MARGIN = 200
    TEXT_ROW_HEIGHT = 50
    
    STAT_TEXT_TOP_COORD = Constants.WINDOW_HEIGHT // 4 - 100
    STAT_TEXT_LEFT_COORD = TEXT_LEFT_MARGIN
    
    BG_COLOR = Constants.AQUAMARINE_BLUE
    GAP_SIZE = 15
    
    FRACTIONAL_PART_LENGTH = 2
    
    def __init__(self, gameDisplay, musicPlayer, statsRepository):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        self.__statsRepository = statsRepository
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(StatsScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        pass
    
    def __convertTime(self, ms):
        minutes = ms / 60000
        ms %= 60000
        seconds = ms / 1000
        ms %= 1000
        return ("%02d:%02d:%03d" % (minutes, seconds, ms)) 
    
    def __displayStat(self, index):
        statistic = self.__statsRepository.statsList[index]
        Text(statistic.description, StatsScreen.TEXT_FONT, StatsScreen.TEXT_FONT_SIZE, StatsScreen.TEXT_COLOR, True).display(self.__gameDisplay, StatsScreen.STAT_TEXT_TOP_COORD + (index + 1) * StatsScreen.TEXT_ROW_HEIGHT + index * StatsScreen.GAP_SIZE, StatsScreen.STAT_TEXT_LEFT_COORD)
        
        quantityText = statistic.quantity
        if statistic.isTime == True:
            quantityText = self.__convertTime(quantityText)
        else: # this is done to ensure that when we have a real number (ex money) it doesn't display like 4.0000000000001
            quantityText = str(quantityText)
            dotPosition = quantityText.find('.')
            if dotPosition != -1 and len(quantityText) - dotPosition > StatsScreen.FRACTIONAL_PART_LENGTH:
                quantityText = quantityText[: dotPosition + StatsScreen.FRACTIONAL_PART_LENGTH]
        
        Text(quantityText, StatsScreen.TEXT_FONT, StatsScreen.TEXT_FONT_SIZE, StatsScreen.TEXT_COLOR, True).display(self.__gameDisplay, StatsScreen.STAT_TEXT_TOP_COORD + (index + 1) * StatsScreen.TEXT_ROW_HEIGHT + index * StatsScreen.GAP_SIZE, StatsScreen.STAT_TEXT_LEFT_COORD + Constants.WINDOW_WIDTH // 2)
    
    def __displayStats(self):
        for index in range(len(self.__statsRepository.statsList)):
            self.__displayStat(index)
    
    def displayContent(self):
        self.setBackgroundImage()
        self.__musicPlayer.displayButtons()
        self.__displayStats()
        pygame.display.update()
        
        mouseX = 0
        mouseY = 0
        mouseClicked = False
        
        while True:
            mouseClicked = False
            pygame.time.wait(1)
             
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__musicPlayer.nextSong()
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    mouseClicked = True
            
            if mouseClicked == True:                    
                self.__musicPlayer.checkInput(mouseX, mouseY)    
                    
                self.setBackgroundImage()
                self.__musicPlayer.displayButtons()   
                self.__displayStats() 
                pygame.display.update()
