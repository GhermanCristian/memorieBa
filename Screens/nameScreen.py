from Screens.screen import Screen
from constants import Constants
import pygame
from pygame.constants import K_RETURN, QUIT, KEYUP, K_ESCAPE, KEYDOWN, K_BACKSPACE, K_RIGHT
from text import Text
from label import Label

class NameScreen(Screen):
    MAX_NAME_LENGTH = 24
    
    TEXT_FONT = "lucidasans"
    TEXT_FONT_SIZE = 20
    TEXT_COLOR = Constants.LIGHT_ORANGE
    TEXT_ROW_HEIGHT = 50
    
    BG_COLOR = Constants.NAVY_BLUE
    LIGHT_BG_COLOR = Constants.GRAY
    
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
        return self.__getPlayerName()
    
    
