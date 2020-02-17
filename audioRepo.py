import os
import pygame
import random
from constants import NORMAL_VOLUME, WELCOME_SONG_PATH

class AudioRepo:
    def __init__(self):
        self.__playlist = []
        self.__songCount = 0
        self.__crtSong = 0
        
        self.__loadPlaylist()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.__introSong = os.path.join(os.getcwd(), WELCOME_SONG_PATH)
        
    def __loadPlaylist(self):
        path = os.path.join(os.getcwd(), "Music")
        
        for file in os.listdir(path):
            if "S_" in file:
                self.__playlist.append(os.path.join(path, file))
                
        self.__songCount = len(self.__playlist)
        random.shuffle(self.__playlist)
        
    def playSong(self):
        pygame.mixer.music.load(self.__playlist[self.__crtSong])
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
        self.__crtSong += 1
        if self.__crtSong >= self.__songCount:
            self.__crtSong = 0
        
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
    def playIntroSong(self):
        pygame.mixer.music.load(self.__introSong)
        pygame.mixer.music.play(-1)   # repeat the song indefinetely
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
        