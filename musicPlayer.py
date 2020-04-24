from text import Text
from button import Button
from playlist import Playlist
from constants import Constants
import pygame

class MusicPlayer():
    TEXT_FONT = "lucidasans"
    TEXT_FONT_SIZE = 20
    TEXT_ROW_HEIGHT = 50
    TEXT_COLOR = Constants.LIGHT_ORANGE
    
    MUSIC_PLAYER_BUTTON_COLOR = Constants.GRAY
    MUSIC_PLAYER_BUTTON_TOP = 400
    MUSIC_PLAYER_BUTTON_LEFT = 35
    MUSIC_PLAYER_BUTTON_SIZE = TEXT_FONT_SIZE
    MUSIC_PLAYER_BUTTON_GAP_SIZE = 5
    
    BALKANIK_FM_LOCATION = "Balkanik FM 0901"
    KITSCH_FM_LOCATION = "Kitsch FM"
    
    #i will create a m.p. object only once, in the mainMenu, and pass it as a parameter to the gameScreen
    def __init__(self, gameDisplay):
        self.__gameDisplay = gameDisplay
        
        self.__completePlaylist = Playlist("")
        self.__completePlaylistNoAds = Playlist("", False)
        self.__balkanikFM = Playlist(MusicPlayer.BALKANIK_FM_LOCATION)
        self.__kitschFM = Playlist(MusicPlayer.KITSCH_FM_LOCATION)
        
        self.__currentPlaylist = self.__completePlaylistNoAds
        
        previousSongButtonText = Text("<", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__previousSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, previousSongButtonText)
        
        pauseSongButtonText = Text("||", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__pauseSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT + MusicPlayer.MUSIC_PLAYER_BUTTON_GAP_SIZE + MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, pauseSongButtonText)
        
        nextSongButtonText = Text(">", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__nextSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT + 2 * MusicPlayer.MUSIC_PLAYER_BUTTON_GAP_SIZE + 2 * MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, nextSongButtonText)
        
    def displayButtons(self):
        self.__previousSongButton.display(self.__gameDisplay)
        self.__pauseSongButton.display(self.__gameDisplay)
        self.__nextSongButton.display(self.__gameDisplay)
    
    def nextSong(self):
        self.__currentPlaylist.nextSong()
        
    def restorePreviousSong(self, previousSongTime):
        self.__currentPlaylist.restorePreviousSong(previousSongTime)
    
    def checkInput(self, mouseX, mouseY):
        if self.__previousSongButton.collides(mouseX, mouseY):
            self.__currentPlaylist.previousSong()
        
        elif self.__pauseSongButton.collides(mouseX, mouseY):
            self.__currentPlaylist.pauseButtonAction()
        
        elif self.__nextSongButton.collides(mouseX, mouseY):
            self.__currentPlaylist.nextSong()
            
    def fadeIn(self):
        vol = pygame.mixer.music.get_volume()
        while vol < Constants.NORMAL_VOLUME:
            vol += Constants.VOLUME_INCREMENT
            pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.set_volume(Constants.NORMAL_VOLUME)
        


