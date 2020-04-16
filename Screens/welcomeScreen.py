from Screens.screen import Screen, QUIT_PROGRAM, CONTINUE_PROGRAM
from constants import WELCOME_SONG_PATH, WINDOW_WIDTH, BG_COLOR, TRANSITION_STEPS, TRANSITION_TIME
from song import Song
import os
import pygame
from pygame.constants import K_RETURN, QUIT, KEYUP, K_ESCAPE

BACKGROUND_IMAGE_TITLE = "WELCOME_SCREEN.jpg"

class WelcomeScreen(Screen):
    def __init__(self, gameDisplay, backgroundSong = WELCOME_SONG_PATH):
        self.__backgroundSong = backgroundSong
        
        self.__backgroundImage = os.path.join(os.getcwd(), "Images")
        self.__backgroundImage = os.path.join(self.__backgroundImage, "Special images")
        self.__backgroundImage = pygame.image.load(os.path.join(self.__backgroundImage, BACKGROUND_IMAGE_TITLE))
        
        self.__gameDisplay = gameDisplay
        
    def setBackgroundImage(self):
        self.__gameDisplay.blit(self.__backgroundImage, (0, 0))
    
    def setBackgroundMusic(self):
        Song(WELCOME_SONG_PATH).play(-1, 0)
    
    def __outroTransition(self):            
        for leftMargin in range(0, WINDOW_WIDTH + 1, WINDOW_WIDTH // TRANSITION_STEPS):
            self.__gameDisplay.fill(BG_COLOR)
            self.__gameDisplay.blit(self.__backgroundImage, (leftMargin, 0))
            pygame.display.update()
            pygame.time.wait(TRANSITION_TIME // TRANSITION_STEPS)
    
    def displayContent(self):
        running = True
        self.setBackgroundMusic()
        while running:
            self.setBackgroundImage()
            for event in pygame.event.get(): 
                if event.type == KEYUP and event.key == K_RETURN:
                    running = False
                    self.__outroTransition()
                elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return QUIT_PROGRAM
            pygame.display.update() 
            
        return CONTINUE_PROGRAM
    
    