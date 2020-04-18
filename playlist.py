import os
import random
import pygame
from song import Song
from constants import NORMAL_VOLUME, VOLUME_INCREMENT

class Playlist():   
    def __init__(self, location = ""):
        self.__songs = []
        self.__songCount = 0
        self.__crtSong = -1
        self.__isPaused = True
        
        self.__path = os.path.join(os.getcwd(), "Music")
        if location != "":
            self.__path = os.path.join(self.__path, location)
            
        self.__delay = 0
        self.__delayFlag = False #when this is True, the delay won't be reset
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.__loadPlaylist()
        
    def __loadPlaylist(self):
        for file in os.listdir(self.__path):
            if file[0] == "S" and file[1] == "_":
                self.__songs.append(Song(os.path.join("Music", file)))
                
        self.__songCount = len(self.__songs)
        random.shuffle(self.__songs)
        
    def nextSong(self, startTime = 0):
        self.__crtSong += 1
        if self.__crtSong >= self.__songCount:
            self.__crtSong = 0
            
        self.__songs[self.__crtSong].play(0, startTime)
            
        # this happens when the song changes (the delay becomes 0 again, because the song has just started)
        if self.__delayFlag == False:
            self.__delay = 0
        self.__delayFlag = False
    
    def previousSong(self, startTime = 0):
        self.__crtSong -= 1
        if self.__crtSong < 0:
            self.__crtSong = self.__songCount - 1
            
        self.__songs[self.__crtSong].play(0, startTime)
        
        if self.__delayFlag == False:
            self.__delay = 0
        self.__delayFlag = False
    
    def pauseButtonAction(self):
        if self.__isPaused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
            
        self.__isPaused = not self.__isPaused
        
    def restorePreviousSong(self, previousSongTime):
        self.__crtSong -= 1
        if self.__crtSong < 0:
            self.__crtSong = self.__songCount - 1
        self.__delayFlag = True
        self.nextSong(previousSongTime + self.__delay)
        self.__delay += previousSongTime

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


