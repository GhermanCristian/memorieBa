import pygame
import os
from constants import APP_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from Screens.screen import QUIT_PROGRAM, CONTINUE_PROGRAM
from Screens.welcomeScreen import WelcomeScreen
from Screens.exitScreen import ExitScreen, EXIT_SCREEN1, EXIT_SCREEN2
from playlist import Playlist
from Screens.nameScreen import NameScreen
from Screens.gameScreen import GameScreen
from Screens.leaderboardScreen import LeaderboardScreen

SERGHEI_ICON = "SERGHEI_ICON.ICO"

class GUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(APP_TITLE)
        
        self.__iconImage = os.path.join(os.getcwd(), "Images")
        self.__iconImage = os.path.join(self.__iconImage, "Special images")
        self.__iconImage = pygame.image.load(os.path.join(self.__iconImage, SERGHEI_ICON))
        
        pygame.display.set_icon(self.__iconImage)
        self.__gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        
        pygame.mouse.set_visible(False)
        
    def __quitGame(self):
        ExitScreen(self.__gameDisplay, EXIT_SCREEN1).displayContent()
        ExitScreen(self.__gameDisplay, EXIT_SCREEN2).displayContent()
        #self.__audioRepo.fadeOut()
        pygame.quit()
        quit()
        
    def start(self):
        programResult = WelcomeScreen(self.__gameDisplay).displayContent()
        if programResult == QUIT_PROGRAM:
            self.__quitGame()
        
        # I will use the same playlist for all the screens (where it applies ofc)
        # bc I don't want to reshuffle the songs each time I create the playlist
        currentPlaylist = Playlist() 
        
        playerName = ""
        programResult = NameScreen(self.__gameDisplay, currentPlaylist).displayContent()
        if programResult == QUIT_PROGRAM:
            self.__quitGame()
        else:
            playerName = programResult
        
        totalTime = 0
        totalMoves = 0
        programResult = GameScreen(self.__gameDisplay, currentPlaylist).displayContent()
        if programResult[0] == QUIT_PROGRAM:
            self.__quitGame()
        else:
            (totalTime, totalMoves) = programResult
        
        programResult = LeaderboardScreen(self.__gameDisplay, currentPlaylist, playerName, totalTime, totalMoves).displayContent()
        if programResult[0] == QUIT_PROGRAM:
            self.__quitGame()
            
        self.__quitGame()
        
        