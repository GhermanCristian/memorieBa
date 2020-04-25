import pygame
import os

class Song():
    def __init__(self, title):
        self.__path = os.path.join(os.getcwd(), title)
        
    def play(self, volume, loops = 0, startTime = 0):
        previousSongTime = pygame.mixer.music.get_pos()
        
        pygame.mixer.music.load(self.__path)
        pygame.mixer.music.play(loops, startTime / 1000)
        pygame.mixer.music.set_volume(volume)
        
        return previousSongTime