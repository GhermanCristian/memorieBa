from Screens.screen import Screen
import pygame
from constants import Constants
from pygame.constants import QUIT, KEYUP, K_ESCAPE, K_RIGHT
from leaderboard import Leaderboard
from text import Text

class LeaderboardScreen(Screen):
    TEXT_FONT = "lucidasans"
    TEXT_FONT_SIZE = 20
    TEXT_COLOR = Constants.LIGHT_ORANGE
    TEXT_LEFT_MARGIN = 35
    TEXT_ROW_HEIGHT = 50
    
    BG_COLOR = Constants.NAVY_BLUE
    
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        
        self.__fastLeader = Leaderboard("fast.pickle")
        self.__smartLeader = Leaderboard("smart.pickle")
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(LeaderboardScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        pass
    
    def __convertTime(self, ms):
        minutes = ms / 60000
        ms %= 60000
        seconds = ms / 1000
        ms %= 1000
        return ("%02d:%02d:%03d" % (minutes, seconds, ms)) 
    
    def __displayResults(self):
        Text("rapidu", LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, Constants.WINDOW_HEIGHT / 4, Constants.WINDOW_WIDTH / 4 - 6 * 7)
        Text("desteptu", LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, Constants.WINDOW_HEIGHT / 4, 3 * Constants.WINDOW_WIDTH / 4 - 6 * 7)
        
        for i in range(Leaderboard.ENTRIES_COUNT):
            Text("%02d. %s" % (i + 1, self.__fastLeader.scoreList[i][0]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + Constants.WINDOW_HEIGHT / 4, 2 * LeaderboardScreen.TEXT_LEFT_MARGIN)
            Text(self.__convertTime(self.__fastLeader.scoreList[i][1]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + Constants.WINDOW_HEIGHT / 4, Constants.WINDOW_WIDTH / 2 - 6 * LeaderboardScreen.TEXT_LEFT_MARGIN)

            Text("%02d. %s" % (i + 1, self.__smartLeader.scoreList[i][0]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + Constants.WINDOW_HEIGHT / 4, Constants.WINDOW_WIDTH / 2 + 2 * LeaderboardScreen.TEXT_LEFT_MARGIN)
            Text("%d moves" % (self.__smartLeader.scoreList[i][1]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + Constants.WINDOW_HEIGHT / 4, Constants.WINDOW_WIDTH - 6 * LeaderboardScreen.TEXT_LEFT_MARGIN)

        pygame.display.update()
    
    def __updateLeaderboard(self, result, leaderboard, playerName):
        newEntry = leaderboard.checkResult(result)
        if newEntry == True:
            leaderboard.addResult(result, playerName)
    
    def updateAllLeaderboards(self, totalTime, totalMoves, playerName):
        self.__updateLeaderboard(totalTime, self.__fastLeader, playerName)
        self.__updateLeaderboard(totalMoves, self.__smartLeader, playerName)
    
    def displayContent(self):
        self.setBackgroundImage()
        self.__displayResults()
        
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__playlist.nextSong()

