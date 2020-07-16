from Screens.screen import Screen
from button import Button
from text import Text
from constants import Constants
from Screens.nameScreen import NameScreen
from Screens.gameScreen import GameScreen
from Screens.leaderboardScreen import LeaderboardScreen
import pygame
from pygame.constants import QUIT, KEYUP, K_ESCAPE, MOUSEMOTION, MOUSEBUTTONUP, K_RIGHT
from musicPlayer import MusicPlayer
from Screens.achievementScreen import AchievementScreen
from statsRepository import StatsRepository

class MainMenuScreen(Screen):
    BG_COLOR = Constants.NAVY_BLUE
    
    TEXT_FONT = "candara"
    TEXT_FONT_SIZE = 26
    TEXT_COLOR = Constants.NORMAL_GREEN
    
    BUTTON_HEIGHT = 100
    BUTTON_WIDTH = 500
    BUTTON_LEFT_COORD = (Constants.WINDOW_WIDTH - BUTTON_WIDTH) // 2
    BUTTON_BACKGROUND_COLOR = Constants.DARK_GREEN
    GAP_SIZE = 30
    
    PLAY_GAME_BUTTON_TOP_COORD = (Constants.WINDOW_HEIGHT - 4 * BUTTON_HEIGHT - 3 * GAP_SIZE) // 2
    LEADERBOARD_BUTTON_TOP_COORD = PLAY_GAME_BUTTON_TOP_COORD + BUTTON_HEIGHT + GAP_SIZE
    ACHIEVEMENT_BUTTON_TOP_COORD = LEADERBOARD_BUTTON_TOP_COORD + BUTTON_HEIGHT + GAP_SIZE
    STATISTICS_BUTTON_TOP_COORD = ACHIEVEMENT_BUTTON_TOP_COORD + BUTTON_HEIGHT + GAP_SIZE
    
    def __init__(self, gameDisplay):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = MusicPlayer(self.__gameDisplay)
        self.__statsRepository = StatsRepository()
        
        self.__mouseX = 0
        self.__mouseY = 0
        self.__mouseClicked = False
        
        self.__leaderboardScreen = LeaderboardScreen(self.__gameDisplay, self.__musicPlayer)
        self.__achievementScreen = AchievementScreen(self.__gameDisplay, self.__musicPlayer, self.__statsRepository)
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(MainMenuScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        self.__musicPlayer.nextSong()
        
    def displayContent(self):
        self.setBackgroundMusic()
        
        playGameText = Text("play game", MainMenuScreen.TEXT_FONT, MainMenuScreen.TEXT_FONT_SIZE, MainMenuScreen.TEXT_COLOR)
        playGameButton = Button(MainMenuScreen.PLAY_GAME_BUTTON_TOP_COORD, MainMenuScreen.BUTTON_LEFT_COORD, MainMenuScreen.BUTTON_WIDTH, MainMenuScreen.BUTTON_HEIGHT, MainMenuScreen.BUTTON_BACKGROUND_COLOR, playGameText)
        
        leaderboardText = Text("hall of fame", MainMenuScreen.TEXT_FONT, MainMenuScreen.TEXT_FONT_SIZE, MainMenuScreen.TEXT_COLOR)
        leaderboardButton = Button(MainMenuScreen.LEADERBOARD_BUTTON_TOP_COORD, MainMenuScreen.BUTTON_LEFT_COORD, MainMenuScreen.BUTTON_WIDTH, MainMenuScreen.BUTTON_HEIGHT, MainMenuScreen.BUTTON_BACKGROUND_COLOR, leaderboardText)
        
        achievementText = Text("achievements", MainMenuScreen.TEXT_FONT, MainMenuScreen.TEXT_FONT_SIZE, MainMenuScreen.TEXT_COLOR)
        achievementButton = Button(MainMenuScreen.ACHIEVEMENT_BUTTON_TOP_COORD, MainMenuScreen.BUTTON_LEFT_COORD, MainMenuScreen.BUTTON_WIDTH, MainMenuScreen.BUTTON_HEIGHT, MainMenuScreen.BUTTON_BACKGROUND_COLOR, achievementText)
        
        statisticsText = Text("stats for nerds", MainMenuScreen.TEXT_FONT, MainMenuScreen.TEXT_FONT_SIZE, MainMenuScreen.TEXT_COLOR)
        statisticsButton = Button(MainMenuScreen.STATISTICS_BUTTON_TOP_COORD, MainMenuScreen.BUTTON_LEFT_COORD, MainMenuScreen.BUTTON_WIDTH, MainMenuScreen.BUTTON_HEIGHT, MainMenuScreen.BUTTON_BACKGROUND_COLOR, statisticsText)
        
        playerName = ""
        totalTime = 0
        totalMoves = 0
        difficulty = Constants.EASY_DIFFICULTY_MULTIPLIER #default value
        
        while True:
            self.__mouseClicked = False
            pygame.time.wait(1)
            
            #this section should only be displayed when the program enters the mainMenu + exits from game/leaderboard etc
            self.setBackgroundImage()
            playGameButton.display(self.__gameDisplay)
            leaderboardButton.display(self.__gameDisplay)
            achievementButton.display(self.__gameDisplay)
            statisticsButton.display(self.__gameDisplay)
            self.__musicPlayer.displayButtons()
            pygame.display.update() 
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
                elif event.type == MOUSEMOTION:
                    self.__mouseX, self.__mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    self.__mouseX, self.__mouseY = event.pos
                    self.__mouseClicked = True
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__musicPlayer.nextSong()
            
            if self.__mouseClicked:
                self.__musicPlayer.checkInput(self.__mouseX, self.__mouseY)
                
                if playGameButton.collides(self.__mouseX, self.__mouseY):
                    programResult = NameScreen(self.__gameDisplay, self.__musicPlayer, self.__statsRepository).displayContent()
                    if programResult[0] == Screen.QUIT_PROGRAM:
                        continue
                    else:
                        (playerName, difficulty) = programResult
                    
                    gameScreen = GameScreen(self.__gameDisplay, self.__musicPlayer, self.__statsRepository)
                    gameScreen.setGameDifficulty(difficulty)
                    programResult = gameScreen.displayContent()
                    if programResult[0] == Screen.QUIT_PROGRAM:
                        continue
                    else:
                        (totalTime, totalMoves) = programResult
                        self.__leaderboardScreen.updateLeaderboards(totalTime, totalMoves, playerName, difficulty)
                        programResult = self.__leaderboardScreen.displayContent()
                        if programResult == Screen.QUIT_PROGRAM:
                            continue
                    
                elif leaderboardButton.collides(self.__mouseX, self.__mouseY):
                    programResult = self.__leaderboardScreen.displayContent()
                    if programResult == Screen.QUIT_PROGRAM:
                        continue
                    
                elif achievementButton.collides(self.__mouseX, self.__mouseY):
                    programResult = self.__achievementScreen.displayContent()
                    if programResult == Screen.QUIT_PROGRAM:
                        continue
                    
                elif statisticsButton.collides(self.__mouseX, self.__mouseY):
                    print ("stats")
                



