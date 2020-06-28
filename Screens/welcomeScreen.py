from Screens.screen import Screen
from constants import Constants
from song import Song
import os
import pygame
from pygame.constants import K_RETURN, QUIT, KEYUP, K_ESCAPE

class WelcomeScreen(Screen):
    IMAGE_TITLE = "WELCOME_SCREEN.jpg"
    SONG_PATH = "Music//W_FRESH.ogg"
    OUTRO_TRANSITION_STEPS = 20
    OUTRO_TRANSITION_TIME = 300
    
    BG_COLOR = Constants.NAVY_BLUE
    
    def __init__(self, gameDisplay):
        self.__backgroundSong = WelcomeScreen.SONG_PATH
        self.__backgroundImage = self.__loadSpecialImage(WelcomeScreen.IMAGE_TITLE)
        
        self.__gameDisplay = gameDisplay
        
    def setBackgroundImage(self):
        self.__gameDisplay.blit(self.__backgroundImage, (0, 0))
    
    def setBackgroundMusic(self):
        Song(WelcomeScreen.SONG_PATH).play(Constants.NORMAL_VOLUME, -1, 0)
        
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
        
    def __outroTransition(self):            
        for leftMargin in range(0, Constants.WINDOW_WIDTH + 1, Constants.WINDOW_WIDTH // WelcomeScreen.OUTRO_TRANSITION_STEPS):
            self.__gameDisplay.fill(WelcomeScreen.BG_COLOR)
            self.__gameDisplay.blit(self.__backgroundImage, (leftMargin, 0))
            pygame.display.update()
            pygame.time.wait(WelcomeScreen.OUTRO_TRANSITION_TIME // WelcomeScreen.OUTRO_TRANSITION_STEPS)
    
    def displayContent(self):
        self.setBackgroundMusic()
        self.setBackgroundImage()
        pygame.display.update() 
        
        while True:
            pygame.time.wait(1)
            
            for event in pygame.event.get(): 
                if event.type == KEYUP and event.key == K_RETURN:
                    self.__outroTransition()
                    return Screen.CONTINUE_PROGRAM
                elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
            
        return Screen.CONTINUE_PROGRAM
    
    