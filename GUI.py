import pygame
import os
from constants import Constants
from Screens.screen import Screen
from Screens.welcomeScreen import WelcomeScreen
from Screens.exitScreen import ExitScreen
from Screens.mainMenuScreen import MainMenuScreen

SERGHEI_ICON = "SERGHEI_ICON.ICO"

class GUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Constants.APP_TITLE)
        
        self.__iconImage = self.__loadSpecialImage(SERGHEI_ICON)
        
        pygame.display.set_icon(self.__iconImage)
        self.__gameDisplay = pygame.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT), pygame.FULLSCREEN)
    
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
        
    def __quitGame(self):
        #ExitScreen(self.__gameDisplay, ExitScreen.EXIT_SCREEN1).displayContent()
        #ExitScreen(self.__gameDisplay, ExitScreen.EXIT_SCREEN2).displayContent()
        pygame.quit()
        quit()
        
    def start(self):
        #programResult = WelcomeScreen(self.__gameDisplay).displayContent()
        #if programResult == Screen.QUIT_PROGRAM:
            #self.__quitGame()
        
        programResult = MainMenuScreen(self.__gameDisplay).displayContent()
        if programResult == Screen.QUIT_PROGRAM:
            self.__quitGame()

        self.__quitGame()
        
        