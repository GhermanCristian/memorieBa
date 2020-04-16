import os
import pygame
import random
from constants import NORMAL_VOLUME, WELCOME_SONG_PATH, VOLUME_INCREMENT, PACANELE_SONG_PATH
from song import Song
from soundCue import SoundCue

class AudioRepo:
    def __init__(self):
        self.__playlist = []
        self.__songCount = 0
        self.__crtSong = 0
        
        self.__loadPlaylist()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.__introSong = Song(os.path.join("Music", WELCOME_SONG_PATH))
        self.__pacaneleSong = Song(os.path.join("Music", PACANELE_SONG_PATH))
        self.__soundCueEndEvent = pygame.USEREVENT + 1
        
        self.__delay = 0
        self.__delayFlag = False #when this is True, the delay won't be reset
        
    def __loadPlaylist(self):
        path = os.path.join(os.getcwd(), "Music")
        
        for file in os.listdir(path):
            if file[0] == "S" and file[1] == "_":
                newSong = Song(os.path.join("Music", file))
                self.__playlist.append(newSong)
                
        self.__songCount = len(self.__playlist)
        random.shuffle(self.__playlist)
        
    def nextSong(self, startTime = 0):
        self.__playlist[self.__crtSong].play(0, startTime)
        
        self.__crtSong += 1
        if self.__crtSong >= self.__songCount:
            self.__crtSong = 0
            
        # this happens when the song changes (the delay becomes 0 again, because the song has just started)
        if self.__delayFlag == False:
            self.__delay = 0
        self.__delayFlag = False
        
    def playIntroSong(self):
        self.__introSong.play(-1, 0)
        
    def playSoundCue(self, soundPath, volMultiplier):
        currentSoundCue = SoundCue(soundPath)
        currentSoundCue.play(volMultiplier)
        
    def playPacaneleSong(self):
        return self.__pacaneleSong.play(-1, 0)
        
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
            pygame.time.wait(5)
        pygame.mixer.music.set_volume(0)
        
    @property
    def soundCueEndEvent(self):
        return self.__soundCueEndEvent
        
        
        
        
        