import pygame
import os
from constants import NORMAL_VOLUME, VOLUME_INCREMENT

class Song():
    def __init__(self, title):
        self.__path = os.path.join(os.getcwd(), title)
        
    def play(self, loops = 0, startTime = 0):
        previousSongTime = pygame.mixer.music.get_pos()
        
        pygame.mixer.music.load(self.__path)
        pygame.mixer.music.play(loops, startTime / 1000)
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
        return previousSongTime
    
    def fadeIn(self):
        vol = pygame.mixer.music.get_volume()
        while vol < NORMAL_VOLUME:
            vol += VOLUME_INCREMENT
            pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
    def fadeOut(self):
        vol = pygame.mixer.music.get_volume()
        while vol > 0.0:
            vol -= 3 * VOLUME_INCREMENT
            pygame.mixer.music.set_volume(vol)
            pygame.time.wait(5)
        pygame.mixer.music.set_volume(0)