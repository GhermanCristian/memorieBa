import pygame

class GameImage():
    def __init__(self, title, fullImagePath, soundCue = None):
        self.__title = title
        self.__fullImagePath = fullImagePath
        self.__soundCue = soundCue
        
    @property
    def title(self):
        return self.__title
    
    @property
    def imageObject(self):
        return pygame.image.load(self.__fullImagePath)
    
    @property
    def soundCue(self):
        return self.__soundCue