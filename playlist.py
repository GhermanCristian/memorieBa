import os
import random
from song import Song

class Playlist():   
    def __init__(self, location = ""):
        self.__songs = []
        self.__songCount = 0
        self.__crtSong = 0
        
        self.__path = os.path.join(os.getcwd(), "Music")
        if location != "":
            self.__path = os.path.join(self.__path, location)
            
        self.__delay = 0
        self.__delayFlag = False #when this is True, the delay won't be reset
        
        self.__loadPlaylist()
        
    def __loadPlaylist(self):
        for file in os.listdir(self.__path):
            if file[0] == "S" and file[1] == "_":
                self.__songs.append(Song(os.path.join("Music", file)))
                
        self.__songCount = len(self.__songs)
        random.shuffle(self.__songs)
        
    def nextSong(self, startTime = 0):
        self.__songs[self.__crtSong].play(0, startTime)
        
        self.__crtSong += 1
        if self.__crtSong >= self.__songCount:
            self.__crtSong = 0
            
        # this happens when the song changes (the delay becomes 0 again, because the song has just started)
        if self.__delayFlag == False:
            self.__delay = 0
        self.__delayFlag = False
        
    def restorePreviousSong(self, previousSongTime):
        self.__crtSong -= 1
        if self.__crtSong < 0:
            self.__crtSong = self.__songCount - 1
        self.__delayFlag = True
        self.nextSong(previousSongTime + self.__delay)
        self.__delay += previousSongTime


