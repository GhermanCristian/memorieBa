from Screens.screen import Screen
from constants import Constants
import pygame
from pygame.constants import K_RETURN, QUIT, KEYUP, K_ESCAPE, KEYDOWN, K_BACKSPACE, K_RIGHT, MOUSEMOTION, MOUSEBUTTONUP
from text import Text
from label import Label
from button import Button
from soundCue import SoundCue

class NameScreen(Screen):
    MAX_NAME_LENGTH = 24
    
    TEXT_FONT = "lucidasans"
    TEXT_FONT_SIZE = 20
    TEXT_COLOR = Constants.LIGHT_ORANGE
    TEXT_ROW_HEIGHT = 50
    TEXT_BOTTOM_MARGIN = 20
    
    BG_COLOR = Constants.NAVY_BLUE
    LIGHT_BG_COLOR = Constants.GRAY
    
    DIFFICULTY_BUTTON_TOP_COORD = Constants.WINDOW_HEIGHT - 300
    DIFFICULTY_BUTTON_SIZE = 150
    DIFFICULTY_BUTTON_GAP_SIZE = 200
    EASY_BUTTON_LEFT_COORD = (Constants.WINDOW_WIDTH - 3 * DIFFICULTY_BUTTON_SIZE - 2 * DIFFICULTY_BUTTON_GAP_SIZE) // 2
    MEDIUM_BUTTON_LEFT_COORD = EASY_BUTTON_LEFT_COORD + DIFFICULTY_BUTTON_SIZE + DIFFICULTY_BUTTON_GAP_SIZE
    HARD_BUTTON_LEFT_COORD = MEDIUM_BUTTON_LEFT_COORD + DIFFICULTY_BUTTON_SIZE + DIFFICULTY_BUTTON_GAP_SIZE
    
    EASY_BUTTON_BG_COLOR = Constants.DARK_GREEN
    MEDIUM_BUTTON_BG_COLOR = Constants.DARK_GREEN
    HARD_BUTTON_BG_COLOR = Constants.DARK_GREEN
    
    def __init__(self, gameDisplay, musicPlayer, statsRepository):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        self.__statsRepository = statsRepository
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(NameScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        pass

    def __displayTextBox(self, userInput):
        userInputText = Text(userInput, NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        Label(Constants.WINDOW_HEIGHT / 2 - NameScreen.TEXT_ROW_HEIGHT / 2, Constants.WINDOW_WIDTH / 2 - 250, 500, NameScreen.TEXT_ROW_HEIGHT, NameScreen.LIGHT_BG_COLOR, userInputText).display(self.__gameDisplay)    
        pygame.display.update()
    
    def __getPlayerName(self):
        userInput = ""
        promptText = Text("baga un nume", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        
        self.setBackgroundImage()
        promptText.display(self.__gameDisplay, Constants.WINDOW_HEIGHT / 2 - 2 * NameScreen.TEXT_ROW_HEIGHT, Constants.WINDOW_WIDTH / 2 - 12 * 7)
        self.__displayTextBox(userInput)
        
        while True:
            pygame.time.wait(1)
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
                if event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__musicPlayer.nextSong()
                if event.type == KEYDOWN:
                    if len(userInput) < NameScreen.MAX_NAME_LENGTH and (event.unicode.isalnum() or event.unicode in "!@#$%^&*()_+-=<>,.?/:{}\|`~ '"):
                        userInput += event.unicode
                        self.__displayTextBox(userInput)
                    elif event.key == K_BACKSPACE:
                        userInput = userInput[:-1]
                        self.__displayTextBox(userInput)
                    elif event.type == SoundCue.SOUND_CUE_END_EVENT:
                        self.__musicPlayer.fadeIn() 
                    elif event.key == K_RETURN:
                        return userInput
    
    def __displayCompletedAchievement(self, achievement):
        if achievement.soundCue != None:
            achievement.soundCue.play()
        
        section = pygame.Rect(NameScreen.EASY_BUTTON_LEFT_COORD, Constants.WINDOW_HEIGHT - NameScreen.TEXT_ROW_HEIGHT - NameScreen.TEXT_BOTTOM_MARGIN, Constants.WINDOW_WIDTH - 2 * NameScreen.EASY_BUTTON_LEFT_COORD, NameScreen.TEXT_ROW_HEIGHT + NameScreen.TEXT_BOTTOM_MARGIN)
        pygame.draw.rect(self.__gameDisplay, NameScreen.BG_COLOR, section)
        Text("Achievement unlocked: %s" % achievement.title, NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR).display(self.__gameDisplay, Constants.WINDOW_HEIGHT - NameScreen.TEXT_ROW_HEIGHT - NameScreen.TEXT_BOTTOM_MARGIN , NameScreen.EASY_BUTTON_LEFT_COORD)
        pygame.display.update(section)
        pygame.time.delay(Constants.COMPLETED_ACHIEVEMENT_DISPLAY_TIME)
        pygame.draw.rect(self.__gameDisplay, NameScreen.BG_COLOR, section) # clear the text
        pygame.display.update(section)
    
    def __processAchievement(self, achievementCheckFunction, *arguments):
        numberOfArguments = {
            self.__statsRepository.setName : 1,
        }
        
        try:
            currentNumberOfArguments = numberOfArguments[achievementCheckFunction]
            
            completedAchievements = []
            # I hope there's a shorter method of doing this, sth more general without needing an if for each no of args
            if currentNumberOfArguments == 1: 
                completedAchievements = achievementCheckFunction(arguments[0])

            for achievement in completedAchievements:
                self.__displayCompletedAchievement(achievement)
                
        except Exception:
            pass        
        
    def __getDifficulty(self):
        easyButtonText = Text("easy", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        easyButton = Button(NameScreen.DIFFICULTY_BUTTON_TOP_COORD, NameScreen.EASY_BUTTON_LEFT_COORD, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.EASY_BUTTON_BG_COLOR, easyButtonText)
        mediumButtonText = Text("medium", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        mediumButton = Button(NameScreen.DIFFICULTY_BUTTON_TOP_COORD, NameScreen.MEDIUM_BUTTON_LEFT_COORD, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.MEDIUM_BUTTON_BG_COLOR, mediumButtonText)
        hardButtonText = Text("hard", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        hardButton = Button(NameScreen.DIFFICULTY_BUTTON_TOP_COORD, NameScreen.HARD_BUTTON_LEFT_COORD, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.HARD_BUTTON_BG_COLOR, hardButtonText)
        
        mouseX = 0
        mouseY = 0
        mouseClicked = False
        
        easyButton.display(self.__gameDisplay)
        mediumButton.display(self.__gameDisplay)
        hardButton.display(self.__gameDisplay)
        pygame.display.update()
        
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
                elif event.type == SoundCue.SOUND_CUE_END_EVENT:
                    self.__musicPlayer.fadeIn()
                    
            if mouseClicked == True:
                if easyButton.collides(mouseX, mouseY):
                    return Constants.EASY_DIFFICULTY_MULTIPLIER
                
                if mediumButton.collides(mouseX, mouseY):
                    return Constants.MEDIUM_DIFFICULTY_MULTIPLIER
                
                if hardButton.collides(mouseX, mouseY):
                    return Constants.HARD_DIFFICULTY_MULTIPLIER
                
    def displayContent(self):
        userName = self.__getPlayerName()
        if (userName == Screen.QUIT_PROGRAM):
            return (Screen.QUIT_PROGRAM, Screen.QUIT_PROGRAM)
        
        self.__processAchievement(self.__statsRepository.setName, userName)
        
        difficulty = self.__getDifficulty()
        if (difficulty == Screen.QUIT_PROGRAM):
            return (Screen.QUIT_PROGRAM, Screen.QUIT_PROGRAM)
        
        return (userName, difficulty)
        
            
            
    
    
