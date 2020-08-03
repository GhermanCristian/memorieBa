from Screens.screen import Screen
import pygame, os
from constants import Constants
from pygame.constants import QUIT, KEYUP, K_ESCAPE, K_RIGHT, MOUSEMOTION, MOUSEBUTTONUP
from leaderboard import Leaderboard
from text import Text
from button import Button
from soundCue import SoundCue

class LeaderboardScreen(Screen):
    TEXT_FONT = "candara"
    TEXT_FONT_SIZE = 30
    TEXT_FONT_CHARACTER_WIDTH = 30
    TEXT_COLOR = Constants.PALE_GOLD
    TEXT_LEFT_MARGIN = 70
    TEXT_ROW_HEIGHT = 50
    
    BG_COLOR = Constants.AQUAMARINE_BLUE
    
    DIFFICULTY_TEXT_TOP_COORD = 80
    DIFFICULTY_TEXT_MID_WEIGHT_COORD = Constants.WINDOW_WIDTH // 2
    
    TITLE_TEXT_TOP_COORD = Constants.WINDOW_HEIGHT // 4 - 100
    TITLE_TEXT_SIZE = 50
    
    DIRECTION_BUTTON_TOP_COORD = Constants.WINDOW_HEIGHT - 80 - 34
    DIRECTION_BUTTON_SIZE = 80
    DIRECTION_BUTTON_COLOR = Constants.NAVY_RED
    DIRECTION_BUTTON_TEXT_SIZE = 40
    PREVIOUS_BUTTON_LEFT_COORD = 500
    NEXT_BUTTON_LEFT_COORD = Constants.WINDOW_WIDTH - 500 - DIRECTION_BUTTON_SIZE
    
    VITEZA_SOUND_CUE = "VITEZA.ogg"
    
    def __init__(self, gameDisplay, musicPlayer):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        
        self.__fastLeaderEasy = Leaderboard("fast_easy.pickle")
        self.__smartLeaderEasy = Leaderboard("smart_easy.pickle")
        self.__fastLeaderMedium = Leaderboard("fast_medium.pickle")
        self.__smartLeaderMedium = Leaderboard("smart_medium.pickle")
        self.__fastLeaderHard = Leaderboard("fast_hard.pickle")
        self.__smartLeaderHard = Leaderboard("smart_hard.pickle")
        
        self.__vitezaSoundCuePath = os.path.join(os.getcwd(), "Music")
        self.__vitezaSoundCuePath = os.path.join(self.__vitezaSoundCuePath, LeaderboardScreen.VITEZA_SOUND_CUE)
        
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
    
    def __displayResults(self, leaderboardDifficulty):
        leaderboardsByDifficulty = [
            (self.__fastLeaderEasy, self.__smartLeaderEasy, "EASY"),
            (self.__fastLeaderMedium, self.__smartLeaderMedium, "MEDIUM"),
            (self.__fastLeaderHard, self.__smartLeaderHard, "HARD")
        ]
        
        Text(leaderboardsByDifficulty[leaderboardDifficulty][2], LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TITLE_TEXT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, LeaderboardScreen.DIFFICULTY_TEXT_TOP_COORD, LeaderboardScreen.DIFFICULTY_TEXT_MID_WEIGHT_COORD - len(leaderboardsByDifficulty[leaderboardDifficulty][2]) * LeaderboardScreen.TEXT_FONT_CHARACTER_WIDTH / 2)
        Text("rapidu", LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, LeaderboardScreen.TITLE_TEXT_TOP_COORD, Constants.WINDOW_WIDTH / 4 - 6 * 7)
        Text("desteptu", LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, LeaderboardScreen.TITLE_TEXT_TOP_COORD, 3 * Constants.WINDOW_WIDTH / 4 - 6 * 7)
        
        for i in range(Leaderboard.ENTRIES_COUNT):
            Text("%02d. %s" % (i + 1, leaderboardsByDifficulty[leaderboardDifficulty][0].scoreList[i][0]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + LeaderboardScreen.TITLE_TEXT_TOP_COORD, LeaderboardScreen.TEXT_LEFT_MARGIN)
            Text(self.__convertTime(leaderboardsByDifficulty[leaderboardDifficulty][0].scoreList[i][1]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + LeaderboardScreen.TITLE_TEXT_TOP_COORD, Constants.WINDOW_WIDTH / 2 - 3 * LeaderboardScreen.TEXT_LEFT_MARGIN)

            Text("%02d. %s" % (i + 1, leaderboardsByDifficulty[leaderboardDifficulty][1].scoreList[i][0]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + LeaderboardScreen.TITLE_TEXT_TOP_COORD, Constants.WINDOW_WIDTH / 2 + LeaderboardScreen.TEXT_LEFT_MARGIN)
            Text("%d moves" % (leaderboardsByDifficulty[leaderboardDifficulty][1].scoreList[i][1]), LeaderboardScreen.TEXT_FONT, LeaderboardScreen.TEXT_FONT_SIZE, LeaderboardScreen.TEXT_COLOR).display(self.__gameDisplay, (i + 2) * LeaderboardScreen.TEXT_ROW_HEIGHT + LeaderboardScreen.TITLE_TEXT_TOP_COORD, Constants.WINDOW_WIDTH - 3 * LeaderboardScreen.TEXT_LEFT_MARGIN)
    
    def __updateLeaderboard(self, result, leaderboard, playerName):
        newEntry = leaderboard.checkResult(result)
        if newEntry == True:
            if result > 400:
            # this means that the result is a totalTime, because it is not feasible that the nr. of moves will be larger than 400
            # and even if it is, it won't get past checkResult, because the last entry in the leaderboard has the same amount of moves
            # on the other hand, no one can finish the game in less than 0.4 seconds, so we are guaranteed to always get here when setting a new time record
                SoundCue(self.__vitezaSoundCuePath).play()
            leaderboard.addResult(result, playerName)
    
    def updateLeaderboards(self, totalTime, totalMoves, playerName, difficulty):
        leaderboardsByDifficulty = {
            Constants.EASY_DIFFICULTY_MULTIPLIER: (self.__fastLeaderEasy, self.__smartLeaderEasy),
            Constants.MEDIUM_DIFFICULTY_MULTIPLIER: (self.__fastLeaderMedium, self.__smartLeaderMedium),
            Constants.HARD_DIFFICULTY_MULTIPLIER: (self.__fastLeaderHard, self.__smartLeaderHard)
        }
        self.__updateLeaderboard(totalTime, leaderboardsByDifficulty[difficulty][0], playerName)
        self.__updateLeaderboard(totalMoves, leaderboardsByDifficulty[difficulty][1], playerName)
    
    def __adjustLeaderboardDifficulty(self, leaderboardDifficulty, increment):
        leaderboardDifficulty += increment
        if leaderboardDifficulty >= Constants.NUMBER_OF_DIFFICULTIES:
            return 0
        if leaderboardDifficulty < 0:
            return Constants.NUMBER_OF_DIFFICULTIES - 1
        return leaderboardDifficulty
    
    def displayContent(self):
        leaderboardDifficulty = 0
        
        previousButtonText = Text("<", LeaderboardScreen.TEXT_FONT, LeaderboardScreen.DIRECTION_BUTTON_TEXT_SIZE, LeaderboardScreen.TEXT_COLOR);
        previousButton = Button(LeaderboardScreen.DIRECTION_BUTTON_TOP_COORD, LeaderboardScreen.PREVIOUS_BUTTON_LEFT_COORD, LeaderboardScreen.DIRECTION_BUTTON_SIZE, LeaderboardScreen.DIRECTION_BUTTON_SIZE, LeaderboardScreen.DIRECTION_BUTTON_COLOR, previousButtonText);
        nextButtonText = Text(">", LeaderboardScreen.TEXT_FONT, LeaderboardScreen.DIRECTION_BUTTON_TEXT_SIZE, LeaderboardScreen.TEXT_COLOR);
        nextButton = Button(LeaderboardScreen.DIRECTION_BUTTON_TOP_COORD, LeaderboardScreen.NEXT_BUTTON_LEFT_COORD, LeaderboardScreen.DIRECTION_BUTTON_SIZE, LeaderboardScreen.DIRECTION_BUTTON_SIZE, LeaderboardScreen.DIRECTION_BUTTON_COLOR, nextButtonText);
        
        self.setBackgroundImage()
        self.__displayResults(leaderboardDifficulty)
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
                    leaderboardDifficulty = self.__adjustLeaderboardDifficulty(leaderboardDifficulty, -1)
                
                elif nextButton.collides(mouseX, mouseY):
                    leaderboardDifficulty = self.__adjustLeaderboardDifficulty(leaderboardDifficulty, 1)
                    
                self.__musicPlayer.checkInput(mouseX, mouseY)    
                    
                self.setBackgroundImage()
                self.__displayResults(leaderboardDifficulty)
                previousButton.display(self.__gameDisplay)
                nextButton.display(self.__gameDisplay)
                self.__musicPlayer.displayButtons()    
                pygame.display.update()

