import pygame
import os
from constants import APP_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from Screens.screen import Screen
from Screens.welcomeScreen import WelcomeScreen
from Screens.exitScreen import ExitScreen
from playlist import Playlist
from Screens.nameScreen import NameScreen
from Screens.gameScreen import GameScreen
from Screens.leaderboardScreen import LeaderboardScreen

SERGHEI_ICON = "SERGHEI_ICON.ICO"

class GUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(APP_TITLE)
        
        self.__iconImage = self.__loadSpecialImage(SERGHEI_ICON)
        
        pygame.display.set_icon(self.__iconImage)
        self.__gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        
        self.__playlist = Playlist()
        
        pygame.mouse.set_visible(False)
    
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
        
    def __quitGame(self):
        #ExitScreen(self.__gameDisplay, ExitScreen.EXIT_SCREEN1).displayContent()
        #ExitScreen(self.__gameDisplay, ExitScreen.EXIT_SCREEN2).displayContent()
        #self.__playlist.fadeOut()
        pygame.quit()
        quit()
        
    def start(self):
        #programResult = WelcomeScreen(self.__gameDisplay).displayContent()
        #if programResult == Screen.QUIT_PROGRAM:
            #self.__quitGame()
        
        playerName = ""
        programResult = NameScreen(self.__gameDisplay, self.__playlist).displayContent()
        if programResult == Screen.QUIT_PROGRAM:
            self.__quitGame()
        else:
            playerName = programResult
        
        totalTime = 0
        totalMoves = 0
        programResult = GameScreen(self.__gameDisplay, self.__playlist).displayContent()
        if programResult[0] == Screen.QUIT_PROGRAM:
            self.__quitGame()
        else:
            (totalTime, totalMoves) = programResult
        
        programResult = LeaderboardScreen(self.__gameDisplay, self.__playlist, playerName, totalTime, totalMoves).displayContent()
        if programResult[0] == Screen.QUIT_PROGRAM:
            self.__quitGame()
            
        self.__quitGame()
        
        