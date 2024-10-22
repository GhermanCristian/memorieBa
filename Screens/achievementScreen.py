from Screens.screen import Screen
from constants import Constants
import pygame
from pygame.constants import QUIT, KEYUP, K_ESCAPE, K_RIGHT, MOUSEMOTION, MOUSEBUTTONUP
from text import Text
from button import Button
from label import Label

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
    
    ELEMENTS_PER_PAGE = 4
    
    PROGRESS_BAR_BG_COLOR = Constants.GRAY
    PROGRESS_BAR_WIDTH = 500
    PROGRESS_BAR_TEXT_COLOR = Constants.BLACK
    PROGRESS_BAR_NOT_COMPLETED_COLOR = Constants.PALE_GOLD
    PROGRESS_BAR_COMPLETED_COLOR = Constants.NORMAL_GREEN
    PROGRESS_BAR_LEFT_COORD = Constants.WINDOW_WIDTH // 2 - 2 * ACHIEVEMENT_TEXT_LEFT_COORD
    
    GAP_SIZE = 15
    
    def __init__(self, gameDisplay, musicPlayer, statsRepository):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        self.__statsRepository = statsRepository
        self.__achievementList = self.__statsRepository.achievementList
        
        self.__page = 0
        self.__totalPages = (len(self.__achievementList) - 1) // AchievementScreen.ELEMENTS_PER_PAGE + 1
        
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
    
    def __displayAchievement(self, index):
        achievement = self.__achievementList[index]
        pagePosition = index % AchievementScreen.ELEMENTS_PER_PAGE
        
        Text(achievement.title, AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.TEXT_COLOR, True).display(self.__gameDisplay, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (pagePosition * 3) * AchievementScreen.TEXT_ROW_HEIGHT + pagePosition * AchievementScreen.GAP_SIZE, AchievementScreen.ACHIEVEMENT_TEXT_LEFT_COORD)
        Text(achievement.description, AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.TEXT_COLOR).display(self.__gameDisplay, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (pagePosition * 3 + 1) * AchievementScreen.TEXT_ROW_HEIGHT + pagePosition * AchievementScreen.GAP_SIZE, AchievementScreen.ACHIEVEMENT_TEXT_LEFT_COORD)
        
        if achievement.prop.checkCompletion() == False:
            pygame.draw.rect(self.__gameDisplay, AchievementScreen.PROGRESS_BAR_BG_COLOR, pygame.Rect(AchievementScreen.PROGRESS_BAR_LEFT_COORD, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (pagePosition * 3 + 1) * AchievementScreen.TEXT_ROW_HEIGHT + pagePosition * AchievementScreen.GAP_SIZE, AchievementScreen.PROGRESS_BAR_WIDTH, AchievementScreen.TEXT_ROW_HEIGHT))
            if achievement.isSecret == False and achievement.completed > 0: # for the secret achievements, the progress is not displayed
                pygame.draw.rect(self.__gameDisplay, AchievementScreen.PROGRESS_BAR_NOT_COMPLETED_COLOR, pygame.Rect(AchievementScreen.PROGRESS_BAR_LEFT_COORD, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (pagePosition * 3 + 1) * AchievementScreen.TEXT_ROW_HEIGHT + pagePosition * AchievementScreen.GAP_SIZE, AchievementScreen.PROGRESS_BAR_WIDTH * achievement.completed // achievement.total, AchievementScreen.TEXT_ROW_HEIGHT))
        else:
            pygame.draw.rect(self.__gameDisplay, AchievementScreen.PROGRESS_BAR_COMPLETED_COLOR, pygame.Rect(AchievementScreen.PROGRESS_BAR_LEFT_COORD, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (pagePosition * 3 + 1) * AchievementScreen.TEXT_ROW_HEIGHT + pagePosition * AchievementScreen.GAP_SIZE, AchievementScreen.PROGRESS_BAR_WIDTH, AchievementScreen.TEXT_ROW_HEIGHT))
            # we add 10 to the top position so that the text is more to the center of the progress bar
            Text("bravo tata, mare pizdar", AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.TEXT_COLOR).display(self.__gameDisplay, AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (pagePosition * 3 + 1) * AchievementScreen.TEXT_ROW_HEIGHT + pagePosition * AchievementScreen.GAP_SIZE + 10, AchievementScreen.PROGRESS_BAR_LEFT_COORD + AchievementScreen.PROGRESS_BAR_WIDTH + AchievementScreen.GAP_SIZE)
        
        if achievement.isSecret == False or (achievement.prop.checkCompletion() == True and achievement.isSecret == True):
            text = Text("%d / %d" % (achievement.completed, achievement.total), AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.PROGRESS_BAR_TEXT_COLOR)
        else:
            text = Text("???", AchievementScreen.TEXT_FONT, AchievementScreen.TEXT_FONT_SIZE, AchievementScreen.PROGRESS_BAR_TEXT_COLOR)
        # we add/ subtract 1 from the label top left coord/ height/ width so that the frame of the rect doesn't overlap with the progress bar (because the frame is 1 pixel thick)
        Label(AchievementScreen.ACHIEVEMENT_TEXT_TOP_COORD + (pagePosition * 3 + 1) * AchievementScreen.TEXT_ROW_HEIGHT + pagePosition * AchievementScreen.GAP_SIZE - 1, AchievementScreen.PROGRESS_BAR_LEFT_COORD - 1, AchievementScreen.PROGRESS_BAR_WIDTH + 1, AchievementScreen.TEXT_ROW_HEIGHT + 1, AchievementScreen.BG_COLOR, text).display(self.__gameDisplay, 1)
    
    def __displayAchievements(self):      
        for index in range(self.__page * AchievementScreen.ELEMENTS_PER_PAGE, min((self.__page + 1) * AchievementScreen.ELEMENTS_PER_PAGE, len(self.__achievementList))):
            self.__displayAchievement(index)
    
    def displayContent(self):
        previousButtonText = Text("<", AchievementScreen.TEXT_FONT, AchievementScreen.DIRECTION_BUTTON_TEXT_SIZE, AchievementScreen.TEXT_COLOR);
        previousButton = Button(AchievementScreen.DIRECTION_BUTTON_TOP_COORD, AchievementScreen.PREVIOUS_BUTTON_LEFT_COORD, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_COLOR, previousButtonText);
        nextButtonText = Text(">", AchievementScreen.TEXT_FONT, AchievementScreen.DIRECTION_BUTTON_TEXT_SIZE, AchievementScreen.TEXT_COLOR);
        nextButton = Button(AchievementScreen.DIRECTION_BUTTON_TOP_COORD, AchievementScreen.NEXT_BUTTON_LEFT_COORD, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_SIZE, AchievementScreen.DIRECTION_BUTTON_COLOR, nextButtonText);
        
        self.__page = 0
        
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

        