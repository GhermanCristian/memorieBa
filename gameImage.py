import pygame

class GameImage():
    def __init__(self, title, fullImagePath, soundCue = None):
        self.__title = title # POZA_1
        self.__fullImagePath = fullImagePath #c ://files//poza_1.jpg
        self.__soundCue = soundCue # Music//SOUND_1.ogg
        
    @property
    def title(self):
        return self.__title
    
    @property
    def imageObject(self):
        return pygame.image.load(self.__fullImagePath)
    
    @property
    def soundCue(self):
        return self.__soundCue