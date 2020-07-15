import os, random, pygame
from song import Song

class Playlist():   
    def __init__(self, radioStation, hasAds = True):
        self.__songs = []
        self.__songCount = 0
        self.__crtSong = -1
        self.__isPaused = True
        
        self.__delay = 0
        self.__delayFlag = False #when this is True, the delay won't be reset
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.__path = os.path.join(os.getcwd(), "Music")
        self.__hasAds = hasAds
        if radioStation == "":
            self.__loadPlaylist("")
        else:
            self.__loadPlaylist(radioStation)
            
        self.__songCount = len(self.__songs)
        random.shuffle(self.__songs)
        
    def __loadPlaylist(self, radioStation):
        path = os.path.join(self.__path, radioStation)
        songFolder = os.path.join("Music", radioStation)
        
        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path, file)):
                self.__loadPlaylist(os.path.join(path, file))
            
            elif "MP3" in radioStation:
                self.__songs.append(Song(os.path.join(songFolder, file)))
            
            elif file[0] == "S" and file[1] == "_":
                if "RECLAMA" in file:
                    if self.__hasAds == True:
                        self.__songs.append(Song(os.path.join(songFolder, file)))
                else:
                    self.__songs.append(Song(os.path.join(songFolder, file)))
        
    def nextSong(self, volume, startTime = 0):
        if (self.__songCount == 0):
            pygame.mixer.music.stop()
            return
        
        self.__isPaused = False
        self.__crtSong += 1
        if self.__crtSong >= self.__songCount:
            self.__crtSong = 0
            
        self.__songs[self.__crtSong].play(volume, 0, startTime)
            
        # this happens when the song changes (the delay becomes 0 again, because the song has just started)
        if self.__delayFlag == False:
            self.__delay = 0
        self.__delayFlag = False
    
    def previousSong(self, volume, startTime = 0):
        if (self.__songCount == 0):
            pygame.mixer.music.stop()
            return
        
        self.__isPaused = False
        self.__crtSong -= 1
        if self.__crtSong < 0:
            self.__crtSong = self.__songCount - 1
            
        self.__songs[self.__crtSong].play(volume, 0, startTime)
        
        if self.__delayFlag == False:
            self.__delay = 0
        self.__delayFlag = False
    
    def pauseButtonAction(self):
        if self.__isPaused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
            
        self.__isPaused = not self.__isPaused
        
    def restorePreviousSong(self, volume, previousSongTime):
        self.__crtSong -= 1
        if self.__crtSong < 0:
            self.__crtSong = self.__songCount - 1
        self.__delayFlag = True
        self.nextSong(volume, previousSongTime + self.__delay)
        self.__delay += previousSongTime
        
    def getCurrentSong(self):
        return self.__songs[self.__crtSong]


