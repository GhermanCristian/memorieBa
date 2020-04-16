from Screens.screen import Screen
import os
import pygame

EXIT_SCREEN1 = "EXIT_SCREEN1.jpg"
EXIT_SCREEN2 = "EXIT_SCREEN2.jpg"

class ExitScreen(Screen):
    def __init__(self, gameDisplay, backgroundImage):
        self.__backgroundImage = os.path.join(os.getcwd(), "Images")
        self.__backgroundImage = os.path.join(self.__backgroundImage, "Special images")
        self.__backgroundImage = pygame.image.load(os.path.join(self.__backgroundImage, backgroundImage))
        
        self.__gameDisplay = gameDisplay
        
    def setBackgroundImage(self):
        self.__gameDisplay.blit(self.__backgroundImage, (0, 0))
        
    def setBackgroundMusic(self):
        pass
    
    def displayContent(self):
        self.setBackgroundImage()
        pygame.display.update()
        pygame.time.wait(2000)