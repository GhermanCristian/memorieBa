from Screens.screen import Screen, QUIT_PROGRAM, CONTINUE_PROGRAM
from constants import BG_COLOR, MAX_NAME_LENGTH, WINDOW_HEIGHT, WINDOW_WIDTH, TEXT_ROW_HEIGHT, LIGHT_BG_COLOR, LIGHT_ORANGE, TEXT_FONT, TEXT_FONT_SIZE
import pygame
from pygame.constants import K_RETURN, QUIT, KEYUP, K_ESCAPE, KEYDOWN, K_BACKSPACE, K_RIGHT
from playlist import Playlist

class NameScreen(Screen):
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        self.__font = pygame.font.SysFont(TEXT_FONT, TEXT_FONT_SIZE, True, False)
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(BG_COLOR)
    
    def setBackgroundMusic(self):
        self.__playlist.nextSong()
    
    def __displayText(self, text, xPos, yPos, font, color):
        self.__gameDisplay.blit(font.render(text, True, color, None), (xPos, yPos))  
    
    def __getPlayerName(self):
        userInput = ""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return QUIT_PROGRAM
                if event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__playlist.nextSong()
                if event.type == KEYDOWN:
                    if len(userInput) < MAX_NAME_LENGTH and (event.unicode.isalnum() or event.unicode in "!@#$%^&*()_+-=<>,.?/:{}\|`~ '"):
                        userInput += event.unicode
                    elif event.key == K_BACKSPACE:
                        userInput = userInput[:-1]
                    elif event.key == K_RETURN:
                        return userInput
                    
            self.setBackgroundImage()
            self.__displayText("baga un nume", WINDOW_WIDTH / 2 - 12 * 7, WINDOW_HEIGHT / 2 - 2 * TEXT_ROW_HEIGHT, self.__font, LIGHT_ORANGE)
            
            pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, (WINDOW_WIDTH / 2 - 250, WINDOW_HEIGHT / 2 - TEXT_ROW_HEIGHT / 2, 500, TEXT_ROW_HEIGHT))
            
            textBlock = self.__font.render(userInput, True, LIGHT_ORANGE)
            textRect = textBlock.get_rect()
            textRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            self.__gameDisplay.blit(textBlock, textRect)
            
            pygame.display.update()
    
    def displayContent(self):
        self.setBackgroundMusic()
        return self.__getPlayerName()
    
    
