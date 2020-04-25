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
    
    MUSIC_PLAYER_BUTTON_SIZE = TEXT_FONT_SIZE
    MUSIC_PLAYER_BUTTON_GAP_SIZE = 5
    RADIO_STATION_PICTURE_TOP = 35
    RADIO_STATION_PICTURE_SIZE = 3 * MUSIC_PLAYER_BUTTON_SIZE + 2 * MUSIC_PLAYER_BUTTON_GAP_SIZE
    RADIO_STATION_PICTURE_LEFT = Constants.WINDOW_WIDTH - RADIO_STATION_PICTURE_SIZE - RADIO_STATION_PICTURE_TOP
    MUSIC_PLAYER_BUTTON_COLOR = Constants.GRAY
    MUSIC_PLAYER_BUTTON_TOP = RADIO_STATION_PICTURE_TOP + RADIO_STATION_PICTURE_SIZE + MUSIC_PLAYER_BUTTON_GAP_SIZE
    MUSIC_PLAYER_BUTTON_LEFT = RADIO_STATION_PICTURE_LEFT
    
    CHANGE_RADIO_STATION_WIDTH = (RADIO_STATION_PICTURE_SIZE - MUSIC_PLAYER_BUTTON_GAP_SIZE) // 2
    CHANGE_RADIO_STATION_HEIGHT = MUSIC_PLAYER_BUTTON_SIZE
    CHANGE_RADIO_STATION_TOP = MUSIC_PLAYER_BUTTON_TOP + MUSIC_PLAYER_BUTTON_SIZE + MUSIC_PLAYER_BUTTON_GAP_SIZE
    PREV_RADIO_STATION_LEFT = RADIO_STATION_PICTURE_LEFT
    NEXT_RADIO_STATION_LEFT = PREV_RADIO_STATION_LEFT + CHANGE_RADIO_STATION_WIDTH + MUSIC_PLAYER_BUTTON_GAP_SIZE
    
    VOLUME_BAR_HEIGHT = MUSIC_PLAYER_BUTTON_SIZE
    VOLUME_BAR_WIDTH = RADIO_STATION_PICTURE_SIZE
    
    RADIO_STATION_COUNT = 4
    BALKANIK_FM_LOCATION = "Balkanik FM 0901"
    KITSCH_FM_LOCATION = "Kitsch FM"
    
    #i will create a m.p. object only once, in the mainMenu, and pass it as a parameter to the gameScreen
    def __init__(self, gameDisplay):
        self.__gameDisplay = gameDisplay
        
        self.__completePlaylist = Playlist("")
        self.__completePlaylistNoAds = Playlist("", False)
        self.__balkanikFM = Playlist(MusicPlayer.BALKANIK_FM_LOCATION)
        self.__kitschFM = Playlist(MusicPlayer.KITSCH_FM_LOCATION)
        
        self.__radioStationList = [
            (self.__completePlaylist, 1),
            (self.__completePlaylistNoAds, 1),
            (self.__balkanikFM, 1),
            (self.__kitschFM, 1)
        ]
        
        self.__currentPlaylistIndex = 0
        
        previousSongButtonText = Text("<", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__previousSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, previousSongButtonText)
        pauseSongButtonText = Text("||", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__pauseSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT + MusicPlayer.MUSIC_PLAYER_BUTTON_GAP_SIZE + MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, pauseSongButtonText)
        nextSongButtonText = Text(">", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__nextSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT + 2 * MusicPlayer.MUSIC_PLAYER_BUTTON_GAP_SIZE + 2 * MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, nextSongButtonText)
        previousRadioStationText = Text("r-", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__previousRadioStationButton = Button(MusicPlayer.CHANGE_RADIO_STATION_TOP, MusicPlayer.PREV_RADIO_STATION_LEFT, MusicPlayer.CHANGE_RADIO_STATION_WIDTH, MusicPlayer.CHANGE_RADIO_STATION_HEIGHT, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, previousRadioStationText)
        nextRadioStationText = Text("r+", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__nextRadioStationButton = Button(MusicPlayer.CHANGE_RADIO_STATION_TOP, MusicPlayer.NEXT_RADIO_STATION_LEFT, MusicPlayer.CHANGE_RADIO_STATION_WIDTH, MusicPlayer.CHANGE_RADIO_STATION_HEIGHT, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, nextRadioStationText)
        
    def displayButtons(self):
        pygame.draw.rect(self.__gameDisplay, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, pygame.Rect(MusicPlayer.RADIO_STATION_PICTURE_LEFT, MusicPlayer.RADIO_STATION_PICTURE_TOP, MusicPlayer.RADIO_STATION_PICTURE_SIZE, MusicPlayer.RADIO_STATION_PICTURE_SIZE))
        self.__previousRadioStationButton.display(self.__gameDisplay)
        self.__nextRadioStationButton.display(self.__gameDisplay)
        self.__previousSongButton.display(self.__gameDisplay)
        self.__pauseSongButton.display(self.__gameDisplay)
        self.__nextSongButton.display(self.__gameDisplay)
    
    def nextSong(self):
        self.__radioStationList[self.__currentPlaylistIndex][0].nextSong()
        
    def restorePreviousSong(self, previousSongTime):
        self.__radioStationList[self.__currentPlaylistIndex][0].restorePreviousSong(previousSongTime)
    
    def __changeRadioStations(self, increment):
        self.__currentPlaylistIndex += increment
        if self.__currentPlaylistIndex >= MusicPlayer.RADIO_STATION_COUNT:
            self.__currentPlaylistIndex = 0
        elif self.__currentPlaylistIndex < 0:
            self.__currentPlaylistIndex = MusicPlayer.RADIO_STATION_COUNT - 1
        
        self.nextSong()
    
    def checkInput(self, mouseX, mouseY):
        if self.__previousSongButton.collides(mouseX, mouseY):
            self.__radioStationList[self.__currentPlaylistIndex][0].previousSong()
        
        elif self.__pauseSongButton.collides(mouseX, mouseY):
            self.__radioStationList[self.__currentPlaylistIndex][0].pauseButtonAction()
        
        elif self.__nextSongButton.collides(mouseX, mouseY):
            self.__radioStationList[self.__currentPlaylistIndex][0].nextSong()
            
        elif self.__previousRadioStationButton.collides(mouseX, mouseY):
            self.__changeRadioStations(-1)
            
        elif self.__nextRadioStationButton.collides(mouseX, mouseY):
            self.__changeRadioStations(1)
            
    def fadeIn(self):
        vol = pygame.mixer.music.get_volume()
        while vol < Constants.NORMAL_VOLUME:
            vol += Constants.VOLUME_INCREMENT
            pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.set_volume(Constants.NORMAL_VOLUME)
        


