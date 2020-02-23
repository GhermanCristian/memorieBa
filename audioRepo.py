import os
import pygame
import random
from constants import NORMAL_VOLUME, WELCOME_SONG_PATH, LOW_VOLUME, VOLUME_INCREMENT, PACANELE_SONG_PATH

class AudioRepo:
    def __init__(self):
        self.__playlist = []
        self.__songCount = 0
        self.__crtSong = 0
        
        self.__loadPlaylist()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.__introSong = os.path.join(os.getcwd(), WELCOME_SONG_PATH)
        self.__pacaneleSong = os.path.join(os.getcwd(), PACANELE_SONG_PATH)
        self.__soundCueEndEvent = pygame.USEREVENT + 1
        
        self.__delay = 0
        self.__delayFlag = False #when this is True, the delay won't be reset
        
    def __loadPlaylist(self):
        path = os.path.join(os.getcwd(), "Music")
        
        for file in os.listdir(path):
            if "S_" in file:
                self.__playlist.append(os.path.join(path, file))
                
        self.__songCount = len(self.__playlist)
        random.shuffle(self.__playlist)
    
    def __playSong(self, song, loops = 0, startTime = 0):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops, startTime / 1000)
        pygame.mixer.music.set_volume(NORMAL_VOLUME)
        
    def nextSong(self, startTime = 0):
        self.__playSong(self.__playlist[self.__crtSong], 0, startTime)
        
        self.__crtSong += 1
        if self.__crtSong >= self.__songCount:
            self.__crtSong = 0
            
        # this happens when the song changes
        if self.__delayFlag == False:
            self.__delay = 0
        self.__delayFlag = False
        
    def playIntroSong(self):
        self.__playSong(self.__introSong, -1, 0)
        
    def playSoundCue(self, soundPath, volMultiplier):
        cue = pygame.mixer.Sound(os.path.join(os.getcwd(), soundPath))
        ch = pygame.mixer.Channel(1)
        ch.play(cue)
        ch.set_endevent(self.__soundCueEndEvent)
        
        pygame.mixer.music.set_volume(LOW_VOLUME)
        cue.set_volume(NORMAL_VOLUME * volMultiplier)
        
    def playPacaneleSong(self):
        prevSongTime = pygame.mixer.music.get_pos()
        self.__playSong(self.__pacaneleSong, -1, 0)
        return prevSongTime
        
    def endPacaneleSong(self, prevSongTime):
        self.__crtSong -= 1
        if self.__crtSong < 0:
            self.__crtSong = self.__songCount - 1
        self.__delayFlag = True
        self.nextSong(prevSongTime + self.__delay)
        self.__delay += prevSongTime
        
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
        
        
        
        
        