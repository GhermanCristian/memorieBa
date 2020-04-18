from Screens.screen import Screen
import pygame
from constants import BG_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH, LIGHT_ORANGE, TEXT_LEFT_MARGIN, TEXT_ROW_HEIGHT,\
    TEXT_FONT, TEXT_FONT_SIZE
from pygame.constants import QUIT, KEYUP, K_ESCAPE, K_RIGHT
from leaderboard import Leaderboard

class LeaderboardScreen(Screen):
    def __init__(self, gameDisplay, playlist, playerName, totalTime, totalMoves):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        self.__font = pygame.font.SysFont(TEXT_FONT, TEXT_FONT_SIZE, True, False)
        
        self.__fastLeader = Leaderboard("fast.pickle")
        self.__smartLeader = Leaderboard("smart.pickle")
        
        self.__playerName = playerName
        self.__totalTime = totalTime
        self.__totalMoves = totalMoves
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(BG_COLOR)
    
    def setBackgroundMusic(self):
        pass
    
    def __displayText(self, text, xPos, yPos, font, color):
        self.__gameDisplay.blit(font.render(text, True, color, None), (xPos, yPos)) 
    
    def __convertTime(self, ms):
        minutes = ms / 60000
        ms %= 60000
        seconds = ms / 1000
        ms %= 1000
        return ("%02d:%02d:%03d" % (minutes, seconds, ms)) 
    
    def __displayResults(self):
        self.__displayText("rapidu", WINDOW_WIDTH / 4 - 6 * 7, WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        self.__displayText("desteptu", 3 * WINDOW_WIDTH / 4 - 6 * 7, WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        
        for i in range(Leaderboard.ENTRIES_COUNT):
            self.__displayText("%02d. %s" % (i + 1, self.__fastLeader.scoreList[i][0]), 2 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            self.__displayText(self.__convertTime(self.__fastLeader.scoreList[i][1]), WINDOW_WIDTH / 2 - 6 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            
            self.__displayText("%02d. %s" % (i + 1, self.__smartLeader.scoreList[i][0]), WINDOW_WIDTH / 2 + 2 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            self.__displayText("%d moves" % (self.__smartLeader.scoreList[i][1]), WINDOW_WIDTH - 6 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        
        pygame.display.update()
    
    def __updateLeaderboard(self, result, leaderboard):
        newEntry = leaderboard.checkResult(result)
        if newEntry == True:
            leaderboard.addResult(result, self.__playerName)
    
    def displayContent(self):
        self.__updateLeaderboard(self.__totalTime, self.__fastLeader)
        self.__updateLeaderboard(self.__totalMoves, self.__smartLeader)
        
        self.setBackgroundImage()
        self.__displayResults()
        
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__playlist.nextSong()

