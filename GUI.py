import pygame
import os
from pygame.constants import *
from constants import *
from leaderboard import Leaderboard
from Screens.screen import QUIT_PROGRAM, CONTINUE_PROGRAM
from Screens.welcomeScreen import WelcomeScreen
from Screens.exitScreen import ExitScreen, EXIT_SCREEN1, EXIT_SCREEN2
from playlist import Playlist
from Screens.nameScreen import NameScreen
from Screens.gameScreen import GameScreen

SERGHEI_ICON = "SERGHEI_ICON.ICO"

class GUI:
    def __init__(self):
        self.__fastLeader = Leaderboard("fast.pickle")
        self.__smartLeader = Leaderboard("smart.pickle")
        
        self.__iconImage = os.path.join(os.getcwd(), "Images")
        self.__iconImage = os.path.join(self.__iconImage, "Special images")
        self.__iconImage = pygame.image.load(os.path.join(self.__iconImage, SERGHEI_ICON))
        
        pygame.init()
        pygame.display.set_caption(APP_TITLE)
        pygame.display.set_icon(self.__iconImage)
        
        self.__gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        
        pygame.mouse.set_visible(False)
        
    def __quitGame(self):
        ExitScreen(self.__gameDisplay, EXIT_SCREEN1).displayContent()
        ExitScreen(self.__gameDisplay, EXIT_SCREEN2).displayContent()
        #self.__audioRepo.fadeOut()
        pygame.quit()
        quit()
    
    def __displayResults(self):
        self.__displayText("rapidu", WINDOW_WIDTH / 4 - 6 * 7, WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        self.__displayText("desteptu", 3 * WINDOW_WIDTH / 4 - 6 * 7, WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        
        for i in range(TABLE_ENTRIES):
            self.__displayText("%02d. %s" % (i + 1, self.__fastLeader.scoreList[i][0]), 2 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            self.__displayText(self.__convertTime(self.__fastLeader.scoreList[i][1]), WINDOW_WIDTH / 2 - 6 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            
            self.__displayText("%02d. %s" % (i + 1, self.__smartLeader.scoreList[i][0]), WINDOW_WIDTH / 2 + 2 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            self.__displayText("%d moves" % (self.__smartLeader.scoreList[i][1]), WINDOW_WIDTH - 6 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        
        pygame.display.update()
    
    def __endGame(self):
        self.__gameDisplay.fill(BG_COLOR)
        self.__displayResults()
        
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.__quitGame()
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__audioRepo.nextSong()
        
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
        
        newFast = self.__fastLeader.checkResult(totalTime)
        if newFast == True:
            self.__fastLeader.addResult(totalTime, playerName)
        newSmart = self.__smartLeader.checkResult(totalMoves)
        if newSmart == True:
            self.__smartLeader.addResult(totalMoves, playerName)
        
        self.__endGame()
        
        