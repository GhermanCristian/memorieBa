import pygame, os
from constants import Constants

class SoundCue():
    SOUND_CUE_END_EVENT = pygame.USEREVENT + 1
    
    def __init__(self, title):
        self.__path = os.path.join(os.getcwd(), title)
    
    def play(self):
        cue = pygame.mixer.Sound(self.__path)
        
        channel = 1
        while pygame.mixer.Channel(channel).get_busy():
            channel += 1
        
        currentVolume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(currentVolume / 4)
        
        currentVolume = min(currentVolume * 2, Constants.MAX_SOUND_CUE_VOLUME)
        currentVolume = max(currentVolume, Constants.MIN_SOUND_CUE_VOLUME)
        
        ch = pygame.mixer.Channel(channel)
        ch.play(cue)
        ch.set_endevent(SoundCue.SOUND_CUE_END_EVENT)
        cue.set_volume(currentVolume)