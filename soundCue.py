import pygame
import os
from constants import Constants

class SoundCue():
    SOUND_CUE_END_EVENT = pygame.USEREVENT + 1
    
    def __init__(self, title):
        self.__path = os.path.join(os.getcwd(), title)
    
    def play(self, volumeMultiplier):
        cue = pygame.mixer.Sound(self.__path)
        
        channel = 1
        while pygame.mixer.Channel(channel).get_busy():
            channel += 1
        
        ch = pygame.mixer.Channel(channel)
        ch.play(cue)
        ch.set_endevent(SoundCue.SOUND_CUE_END_EVENT)
        
        pygame.mixer.music.set_volume(Constants.LOW_VOLUME)
        cue.set_volume(Constants.NORMAL_VOLUME * volumeMultiplier)