import os
import pygame
import random
from constants import NORMAL_VOLUME, WELCOME_SONG_PATH, LOW_VOLUME, VOLUME_INCREMENT

class AudioRepo:
    def __init__(self):
        self.__playlist = []
        self.__songCount = 0
        self.__crtSong = 0
        
        self.__loadPlaylist()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.__introSong = os.path.join(os.getcwd(), WELCOME_SONG_PATH)
        self.__soundCueEndEvent = pygame.USEREVENT + 1
        
    def __loadPlaylist(self):
        path = os.path.join(os.getcwd(), "Music")
        
        for file in os.listdir(path):
            if "S_" in file:
                self.__playlist.append(os.path.join(path, file))
                
        self.__songCount = len(self.__playlist)
        random.shuffle(self.__playlist)
        
    def playSong(self, startTime = 0):
        pygame.mixer.music.load(self.__playlist[self.__crtSong])
        pygame.mixer.music.play(0, startTime // 1000)
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
        self.__crtSong += 1
        if self.__crtSong >= self.__songCount:
            self.__crtSong = 0
        
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
    def playIntroSong(self):
        pygame.mixer.music.load(self.__introSong)
        pygame.mixer.music.play(-1)   # repeat the song indefinitely
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
    def playSoundCue(self, soundPath, volMultiplier):
        cue = pygame.mixer.Sound(os.path.join(os.getcwd(), soundPath))
        ch = pygame.mixer.Channel(1)
        ch.play(cue)
        ch.set_endevent(self.__soundCueEndEvent)
        
        pygame.mixer.music.set_volume(LOW_VOLUME)
        cue.set_volume(NORMAL_VOLUME * volMultiplier)
        
    def playPacaneleSong(self):
        prevSongTime = pygame.mixer.music.get_pos() + 100
        pygame.mixer.music.load(self.__introSong)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
        return prevSongTime
        
    def endPacaneleSong(self, prevSongTime):
        self.__crtSong -= 1
        if self.__crtSong < 0:
            self.__crtSong = self.__songCount - 1
        self.playSong(prevSongTime)
        
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
        pygame.mixer.music.set_volume(0)
        
    @property
    def soundCueEndEvent(self):
        return self.__soundCueEndEvent
        
        
        
        
        