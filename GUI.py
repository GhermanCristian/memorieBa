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
        currentImage = os.path.join(currentImage, "Special_images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
        
    def __quitGame(self):
        ExitScreen(self.__gameDisplay, ExitScreen.EXIT_SCREEN1).displayContent()
        ExitScreen(self.__gameDisplay, ExitScreen.EXIT_SCREEN2).displayContent()
        ExitScreen(self.__gameDisplay, ExitScreen.EXIT_SCREEN3).displayContent()
        pygame.quit()
        
    def start(self):
        programResult = WelcomeScreen(self.__gameDisplay).displayContent()
        if programResult == Screen.QUIT_PROGRAM:
            self.__quitGame()
            return 
            #I have to add this return because pygame.quit() doesn't actually quit the program, just pygame
            #that's why there was the issue with the font not being initialised (because at that point pygame was not initialised)
        
        #normally I would have to store the programResult and check for QUIT_PROGRAM, like above;
        #but this is techically the last screen we interact with, so I would've had quit on both branches of if/else
        #so I just removed the if/else altogether
        MainMenuScreen(self.__gameDisplay).displayContent()
        self.__quitGame()
        
        