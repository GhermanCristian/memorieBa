import os
import pygame
import random
from constants import NORMAL_VOLUME, WELCOME_SONG_PATH, VOLUME_INCREMENT, PACANELE_SONG_PATH
from song import Song
from playlist import Playlist
from soundCue import SoundCue

class AudioRepo:
    def __init__(self):
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.__introSong = Song(WELCOME_SONG_PATH)
        self.__pacaneleSong = Song(PACANELE_SONG_PATH)
        self.__soundCueEndEvent = pygame.USEREVENT + 1
        
        self.__playlist = Playlist()
        
    def nextSong(self, startTime = 0):
        self.__playlist.nextSong(startTime)
        
    def playIntroSong(self):
        self.__introSong.play(-1, 0)
        
    def playSoundCue(self, soundPath, volMultiplier):
        currentSoundCue = SoundCue(soundPath)
        currentSoundCue.play(volMultiplier)
        
    def playPacaneleSong(self):
        return self.__pacaneleSong.play(-1, 0)
        
    def endPacaneleSong(self, prevSongTime):
        self.__playlist.restorePreviousSong(prevSongTime)
        
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
        
        
        
        
        