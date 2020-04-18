from Screens.screen import Screen
from constants import BG_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH, TEXT_ROW_HEIGHT, LIGHT_BG_COLOR, LIGHT_ORANGE, TEXT_FONT, TEXT_FONT_SIZE
import pygame
from pygame.constants import K_RETURN, QUIT, KEYUP, K_ESCAPE, KEYDOWN, K_BACKSPACE, K_RIGHT
from text import Text
from label import Label

class NameScreen(Screen):
    MAX_NAME_LENGTH = 24
    
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(BG_COLOR)
    
    def setBackgroundMusic(self):
        self.__playlist.nextSong()

    def __getPlayerName(self):
        userInput = ""
        promptText = Text("baga un nume", TEXT_FONT, TEXT_FONT_SIZE, LIGHT_ORANGE)
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
            promptText.display(self.__gameDisplay, WINDOW_HEIGHT / 2 - 2 * TEXT_ROW_HEIGHT, WINDOW_WIDTH / 2 - 12 * 7)
            userInputText = Text(userInput, TEXT_FONT, TEXT_FONT_SIZE, LIGHT_ORANGE)
            Label(WINDOW_HEIGHT / 2 - TEXT_ROW_HEIGHT / 2, WINDOW_WIDTH / 2 - 250, 500, TEXT_ROW_HEIGHT, LIGHT_BG_COLOR, userInputText).display(self.__gameDisplay)
            
            pygame.display.update()
    
    def displayContent(self):
        self.setBackgroundMusic()
        return self.__getPlayerName()
    
    
