from Screens.screen import Screen
from constants import Constants
import pygame
from pygame.constants import K_RETURN, QUIT, KEYUP, K_ESCAPE, KEYDOWN, K_BACKSPACE, K_RIGHT, MOUSEMOTION, MOUSEBUTTONUP
from text import Text
from label import Label
from button import Button

class NameScreen(Screen):
    MAX_NAME_LENGTH = 24
    
    TEXT_FONT = "lucidasans"
    TEXT_FONT_SIZE = 20
    TEXT_COLOR = Constants.LIGHT_ORANGE
    TEXT_ROW_HEIGHT = 50
    
    BG_COLOR = Constants.NAVY_BLUE
    LIGHT_BG_COLOR = Constants.GRAY
    
    EASY_DIFFICULTY_MULTIPLIER = 1.0
    MEDIUM_DIFFICULTY_MULTIPLIER = 1.5
    HARD_DIFFICULTY_MULTIPLIER = 2.0
    
    DIFFICULTY_BUTTON_TOP_COORD = Constants.WINDOW_HEIGHT - 300
    DIFFICULTY_BUTTON_SIZE = 150
    DIFFICULTY_BUTTON_GAP_SIZE = 200
    EASY_BUTTON_LEFT_COORD = (Constants.WINDOW_WIDTH - 3 * DIFFICULTY_BUTTON_SIZE - 2 * DIFFICULTY_BUTTON_GAP_SIZE) // 2
    MEDIUM_BUTTON_LEFT_COORD = EASY_BUTTON_LEFT_COORD + DIFFICULTY_BUTTON_SIZE + DIFFICULTY_BUTTON_GAP_SIZE
    HARD_BUTTON_LEFT_COORD = MEDIUM_BUTTON_LEFT_COORD + DIFFICULTY_BUTTON_SIZE + DIFFICULTY_BUTTON_GAP_SIZE
    
    EASY_BUTTON_BG_COLOR = Constants.DARK_GREEN
    MEDIUM_BUTTON_BG_COLOR = Constants.DARK_GREEN
    HARD_BUTTON_BG_COLOR = Constants.DARK_GREEN
    
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(NameScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        pass

    def __getPlayerName(self):
        userInput = ""
        promptText = Text("baga un nume", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
                if event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__playlist.nextSong()
                if event.type == KEYDOWN:
                    if len(userInput) < NameScreen.MAX_NAME_LENGTH and (event.unicode.isalnum() or event.unicode in "!@#$%^&*()_+-=<>,.?/:{}\|`~ '"):
                        userInput += event.unicode
                    elif event.key == K_BACKSPACE:
                        userInput = userInput[:-1]
                    elif event.key == K_RETURN:
                        return userInput
                    
            self.setBackgroundImage()
            promptText.display(self.__gameDisplay, Constants.WINDOW_HEIGHT / 2 - 2 * NameScreen.TEXT_ROW_HEIGHT, Constants.WINDOW_WIDTH / 2 - 12 * 7)
            userInputText = Text(userInput, NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
            Label(Constants.WINDOW_HEIGHT / 2 - NameScreen.TEXT_ROW_HEIGHT / 2, Constants.WINDOW_WIDTH / 2 - 250, 500, NameScreen.TEXT_ROW_HEIGHT, NameScreen.LIGHT_BG_COLOR, userInputText).display(self.__gameDisplay)
            
            pygame.display.update()
    
    def displayContent(self):
        userName = self.__getPlayerName()
        
        if (userName == Screen.QUIT_PROGRAM):
            return (Screen.QUIT_PROGRAM, Screen.QUIT_PROGRAM)
        
        easyButtonText = Text("easy", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        easyButton = Button(NameScreen.DIFFICULTY_BUTTON_TOP_COORD, NameScreen.EASY_BUTTON_LEFT_COORD, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.EASY_BUTTON_BG_COLOR, easyButtonText)
        mediumButtonText = Text("medium", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        mediumButton = Button(NameScreen.DIFFICULTY_BUTTON_TOP_COORD, NameScreen.MEDIUM_BUTTON_LEFT_COORD, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.MEDIUM_BUTTON_BG_COLOR, mediumButtonText)
        hardButtonText = Text("hard", NameScreen.TEXT_FONT, NameScreen.TEXT_FONT_SIZE, NameScreen.TEXT_COLOR)
        hardButton = Button(NameScreen.DIFFICULTY_BUTTON_TOP_COORD, NameScreen.HARD_BUTTON_LEFT_COORD, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.DIFFICULTY_BUTTON_SIZE, NameScreen.HARD_BUTTON_BG_COLOR, hardButtonText)
        
        mouseX = 0
        mouseY = 0
        mouseClicked = False
        
        while True:
            mouseClicked = False
            
            easyButton.display(self.__gameDisplay)
            mediumButton.display(self.__gameDisplay)
            hardButton.display(self.__gameDisplay)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return (Screen.QUIT_PROGRAM, Screen.QUIT_PROGRAM)
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__playlist.nextSong()
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    mouseClicked = True
                    
            if mouseClicked == True:
                if easyButton.collides(mouseX, mouseY):
                    return (userName, NameScreen.EASY_DIFFICULTY_MULTIPLIER)
                
                if mediumButton.collides(mouseX, mouseY):
                    return (userName, NameScreen.MEDIUM_DIFFICULTY_MULTIPLIER)
                
                if hardButton.collides(mouseX, mouseY):
                    return (userName, NameScreen.HARD_DIFFICULTY_MULTIPLIER)
            
            
    
    
