from Screens.screen import Screen
from constants import Constants
import pygame
from pygame.constants import QUIT, KEYUP, K_ESCAPE, K_RIGHT, MOUSEMOTION, MOUSEBUTTONUP
from text import Text
from button import Button

class AchievementScreen(Screen):
    TEXT_FONT = "candara"
    TEXT_FONT_SIZE = 26
    TEXT_FONT_CHARACTER_WIDTH = 26
    TEXT_COLOR = Constants.PALE_GOLD
    TEXT_LEFT_MARGIN = 100
    TEXT_ROW_HEIGHT = 44
    
    BG_COLOR = Constants.AQUAMARINE_BLUE
    
    DIRECTION_BUTTON_TOP_COORD = Constants.WINDOW_HEIGHT - 80 - 34
    DIRECTION_BUTTON_SIZE = 80
    DIRECTION_BUTTON_COLOR = Constants.NAVY_RED
    DIRECTION_BUTTON_TEXT_SIZE = 40
    PREVIOUS_BUTTON_LEFT_COORD = 500
    NEXT_BUTTON_LEFT_COORD = Constants.WINDOW_WIDTH - 500 - DIRECTION_BUTTON_SIZE
    
    ACHIEVEMENT_TEXT_TOP_COORD = Constants.WINDOW_HEIGHT // 4 - 100
    ACHIEVEMENT_TEXT_LEFT_COORD = TEXT_LEFT_MARGIN
    
    ELEMENTS_PER_PAGE = 10
    
    LIGHT_BG_COLOR = Constants.GRAY
    PROGRESS_BAR_WIDTH = 500
    
    def __init__(self, gameDisplay, musicPlayer, statsRepository):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        self.__statsRepository = statsRepository
        self.__achievementList = self.__statsRepository.achievementList
        
        self.__page = 0
        self.__totalPages = len(self.__statsRepository.achievementList) // AchievementScreen.ELEMENTS_PER_PAGE + 1
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(AchievementScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        pass
    
    def __changePage(self, increment):
        self.__page += increment
        
        if self.__page < 0:
            self.__page = self.__totalPages - 1;
        elif self.__page >= self.__totalPages:
            self.__page = 0
    
    def __displayAchievement(self, indexOnPage):
        achievement = self.__achievementList[indexOnPage]
        Text(achievement.title, AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.TEXT_COLOR).display(self.__gameDisplay, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (indexOnPage * 3) * AchievementScreen.TEXT_ROW_HEIGHT, AchievementScreen.ACHIEVEMENT_TEXT_LEFT_COORD)
        Text(achievement.description, AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.TEXT_COLOR).display(self.__gameDisplay, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (indexOnPage * 3 + 1) * AchievementScreen.TEXT_ROW_HEIGHT, AchievementScreen.ACHIEVEMENT_TEXT_LEFT_COORD)
        pygame.draw.rect(self.__gameDisplay, AchievementScreen.LIGHT_BG_COLOR, pygame.Rect(AchievementScreen.ACHIEVEMENT_TEXT_LEFT_COORD, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (indexOnPage * 3 + 2) * AchievementScreen.TEXT_ROW_HEIGHT, AchievementScreen.PROGRESS_BAR_WIDTH, AchievementScreen.TEXT_ROW_HEIGHT))
        if achievement.completed != 0:
            pygame.draw.rect(self.__gameDisplay, AchievementScreen.TEXT_COLOR, pygame.Rect(AchievementScreen.ACHIEVEMENT_TEXT_LEFT_COORD, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (indexOnPage * 3 + 2) * AchievementScreen.TEXT_ROW_HEIGHT, AchievementScreen.PROGRESS_BAR_WIDTH * achievement.completed // achievement.total, AchievementScreen.TEXT_ROW_HEIGHT))
        Text("%d / %d" % (achievement.completed, achievement.total), AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.TEXT_COLOR).display(self.__gameDisplay, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (indexOnPage * 3 + 2) * AchievementScreen.TEXT_ROW_HEIGHT, AchievementScreen.ACHIEVEMENT_TEXT_LEFT_COORD)
    
    def __displayAchievements(self):
        # this min can be removed when we'll have more than 1 page of achievements        
        for index in range(self.__page * AchievementScreen.ELEMENTS_PER_PAGE, min((self.__page + 1) * AchievementScreen.ELEMENTS_PER_PAGE, len(self.__achievementList))):
            self.__displayAchievement(index)
    
    def displayContent(self):
        previousButtonText = Text("<", AchievementScreen.TEXT_FONT, AchievementScreen.DIRECTION_BUTTON_TEXT_SIZE, AchievementScreen.TEXT_COLOR);
        previousButton = Button(AchievementScreen.DIRECTION_BUTTON_TOP_COORD, AchievementScreen.PREVIOUS_BUTTON_LEFT_COORD, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_COLOR, previousButtonText);
        nextButtonText = Text(">", AchievementScreen.TEXT_FONT, AchievementScreen.DIRECTION_BUTTON_TEXT_SIZE, AchievementScreen.TEXT_COLOR);
        nextButton = Button(AchievementScreen.DIRECTION_BUTTON_TOP_COORD, AchievementScreen.NEXT_BUTTON_LEFT_COORD, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_COLOR, nextButtonText);
        
        self.setBackgroundImage()
        self.__displayAchievements()
        previousButton.display(self.__gameDisplay)
        nextButton.display(self.__gameDisplay)
        self.__musicPlayer.displayButtons()
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
                if previousButton.collides(mouseX, mouseY):
                    self.__changePage(-1)
                
                elif nextButton.collides(mouseX, mouseY):
                    self.__changePage(1)
                    
                self.__musicPlayer.checkInput(mouseX, mouseY)    
                    
                self.setBackgroundImage()
                self.__displayAchievements()
                previousButton.display(self.__gameDisplay)
                nextButton.display(self.__gameDisplay)
                self.__musicPlayer.displayButtons()    
                pygame.display.update()

        