from text import Text
from button import Button
from playlist import Playlist
from soundCue import SoundCue
from constants import Constants
import pygame
import os

class MusicPlayer():
    TEXT_FONT = "lucidasans"
    TEXT_FONT_SIZE = 28
    TEXT_COLOR = Constants.LIGHT_ORANGE
    
    MUSIC_PLAYER_BUTTON_SIZE = TEXT_FONT_SIZE
    MUSIC_PLAYER_BUTTON_GAP_SIZE = MUSIC_PLAYER_BUTTON_SIZE // 4 - 3
    RADIO_STATION_PICTURE_TOP = 35
    RADIO_STATION_PICTURE_SIZE = 3 * MUSIC_PLAYER_BUTTON_SIZE + 2 * MUSIC_PLAYER_BUTTON_GAP_SIZE # 92 pixels
    RADIO_STATION_PICTURE_LEFT = Constants.WINDOW_WIDTH - RADIO_STATION_PICTURE_SIZE - RADIO_STATION_PICTURE_TOP
    MUSIC_PLAYER_BUTTON_COLOR = Constants.GRAY
    MUSIC_PLAYER_BUTTON_TOP = RADIO_STATION_PICTURE_TOP + RADIO_STATION_PICTURE_SIZE + MUSIC_PLAYER_BUTTON_GAP_SIZE
    MUSIC_PLAYER_BUTTON_LEFT = RADIO_STATION_PICTURE_LEFT
    
    CHANGE_RADIO_STATION_WIDTH = (RADIO_STATION_PICTURE_SIZE - MUSIC_PLAYER_BUTTON_GAP_SIZE) // 2
    CHANGE_RADIO_STATION_HEIGHT = MUSIC_PLAYER_BUTTON_SIZE
    CHANGE_RADIO_STATION_TOP = MUSIC_PLAYER_BUTTON_TOP + MUSIC_PLAYER_BUTTON_SIZE + MUSIC_PLAYER_BUTTON_GAP_SIZE
    PREV_RADIO_STATION_LEFT = RADIO_STATION_PICTURE_LEFT
    NEXT_RADIO_STATION_LEFT = PREV_RADIO_STATION_LEFT + CHANGE_RADIO_STATION_WIDTH + MUSIC_PLAYER_BUTTON_GAP_SIZE
    
    VOLUME_BAR_HEIGHT = MUSIC_PLAYER_BUTTON_SIZE // 2
    VOLUME_BAR_WIDTH = RADIO_STATION_PICTURE_SIZE
    VOLUME_BAR_TOP = CHANGE_RADIO_STATION_TOP + CHANGE_RADIO_STATION_HEIGHT + MUSIC_PLAYER_BUTTON_GAP_SIZE
    VOLUME_BAR_LEFT = RADIO_STATION_PICTURE_LEFT
    
    RADIO_STATION_COUNT = 5
    BALKANIK_FM_LOCATION = "Balkanik FM 0901"
    BALKANIK_FM_IMAGE = "BALKANIK_FM.jpg"
    KITSCH_FM_LOCATION = "Kitsch FM"
    KITSCH_FM_IMAGE = "KITSCH_FM.jpg"
    RADIO_CONTACT_IMAGE = "RADIO_CONTACT.jpg"
    RADIO_CONTACT_NO_ADS_IMAGE = "RADIO_CONTACT_NO_ADS.jpg"
    MP3_PLAYER_LOCATION = "MP3"
    MP3_PLAYER_IMAGE = "MP3_PLAYER.jpg"
    RADIO_CHANGING_SOUND_LOCATION = os.path.join("Music", "RADIO_CHANGING_SOUND.ogg")
    
    #i will create a m.p. object only once, in the mainMenu, and pass it as a parameter to the gameScreen
    def __init__(self, gameDisplay):
        self.__gameDisplay = gameDisplay
        
        self.__completePlaylist = Playlist("") #Radio Contact
        self.__completePlaylistNoAds = Playlist("", False) 
        self.__balkanikFM = Playlist(MusicPlayer.BALKANIK_FM_LOCATION)
        self.__kitschFM = Playlist(MusicPlayer.KITSCH_FM_LOCATION)
        self.__MP3Player = Playlist(MusicPlayer.MP3_PLAYER_LOCATION)
        self.__radioChangingSound = SoundCue(MusicPlayer.RADIO_CHANGING_SOUND_LOCATION)
        
        self.__radioContactImage = self.__loadSpecialImage(MusicPlayer.RADIO_CONTACT_IMAGE)
        self.__radioContactNoAdsImage = self.__loadSpecialImage(MusicPlayer.RADIO_CONTACT_NO_ADS_IMAGE)
        self.__balkanikFMImage = self.__loadSpecialImage(MusicPlayer.BALKANIK_FM_IMAGE)
        self.__kitschFMImage = self.__loadSpecialImage(MusicPlayer.KITSCH_FM_IMAGE)
        self.__MP3PlayerImage = self.__loadSpecialImage(MusicPlayer.MP3_PLAYER_IMAGE)
        
        self.__radioStationList = [
            (self.__completePlaylist, self.__radioContactImage),
            (self.__completePlaylistNoAds, self.__radioContactNoAdsImage),
            (self.__balkanikFM, self.__balkanikFMImage),
            (self.__kitschFM, self.__kitschFMImage),
            (self.__MP3Player, self.__MP3PlayerImage)
        ]
        
        self.__currentPlaylistIndex = 0
        self.__musicVolume = Constants.NORMAL_VOLUME
        
        previousSongButtonText = Text("<", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__previousSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, previousSongButtonText)
        pauseSongButtonText = Text("||", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__pauseSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT + MusicPlayer.MUSIC_PLAYER_BUTTON_GAP_SIZE + MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, pauseSongButtonText)
        nextSongButtonText = Text(">", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__nextSongButton = Button(MusicPlayer.MUSIC_PLAYER_BUTTON_TOP, MusicPlayer.MUSIC_PLAYER_BUTTON_LEFT + 2 * MusicPlayer.MUSIC_PLAYER_BUTTON_GAP_SIZE + 2 * MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_SIZE, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, nextSongButtonText)
        previousRadioStationText = Text("R-", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__previousRadioStationButton = Button(MusicPlayer.CHANGE_RADIO_STATION_TOP, MusicPlayer.PREV_RADIO_STATION_LEFT, MusicPlayer.CHANGE_RADIO_STATION_WIDTH, MusicPlayer.CHANGE_RADIO_STATION_HEIGHT, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, previousRadioStationText)
        nextRadioStationText = Text("R+", MusicPlayer.TEXT_FONT, MusicPlayer.TEXT_FONT_SIZE, MusicPlayer.TEXT_COLOR)
        self.__nextRadioStationButton = Button(MusicPlayer.CHANGE_RADIO_STATION_TOP, MusicPlayer.NEXT_RADIO_STATION_LEFT, MusicPlayer.CHANGE_RADIO_STATION_WIDTH, MusicPlayer.CHANGE_RADIO_STATION_HEIGHT, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, nextRadioStationText)
        self.__volumeBarButton = Button(MusicPlayer.VOLUME_BAR_TOP, MusicPlayer.VOLUME_BAR_LEFT, MusicPlayer.VOLUME_BAR_WIDTH, MusicPlayer.VOLUME_BAR_HEIGHT, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, None)
        self.__currentVolumeBarButton = Button(MusicPlayer.VOLUME_BAR_TOP, MusicPlayer.VOLUME_BAR_LEFT, self.__musicVolume * MusicPlayer.VOLUME_BAR_WIDTH, MusicPlayer.VOLUME_BAR_HEIGHT, MusicPlayer.MUSIC_PLAYER_BUTTON_COLOR, None)
    
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
        
    def displayButtons(self):
        self.__gameDisplay.blit(self.__radioStationList[self.__currentPlaylistIndex][1], (MusicPlayer.RADIO_STATION_PICTURE_LEFT, MusicPlayer.RADIO_STATION_PICTURE_TOP))
        self.__previousRadioStationButton.display(self.__gameDisplay)
        self.__nextRadioStationButton.display(self.__gameDisplay)
        self.__previousSongButton.display(self.__gameDisplay)
        self.__pauseSongButton.display(self.__gameDisplay)
        self.__nextSongButton.display(self.__gameDisplay)
        self.__volumeBarButton.display(self.__gameDisplay)
        Button(MusicPlayer.VOLUME_BAR_TOP, MusicPlayer.VOLUME_BAR_LEFT, self.__musicVolume * MusicPlayer.VOLUME_BAR_WIDTH, MusicPlayer.VOLUME_BAR_HEIGHT, MusicPlayer.TEXT_COLOR, None).display(self.__gameDisplay)
    
    def nextSong(self):
        self.__radioStationList[self.__currentPlaylistIndex][0].nextSong(self.__musicVolume)
        
    def restorePreviousSong(self, previousSongTime):
        self.__radioStationList[self.__currentPlaylistIndex][0].restorePreviousSong(self.__musicVolume, previousSongTime)
    
    def __changeRadioStations(self, increment):
        self.__radioChangingSound.play()
        self.__currentPlaylistIndex += increment
        if self.__currentPlaylistIndex >= MusicPlayer.RADIO_STATION_COUNT:
            self.__currentPlaylistIndex = 0
        elif self.__currentPlaylistIndex < 0:
            self.__currentPlaylistIndex = MusicPlayer.RADIO_STATION_COUNT - 1
        
        pygame.time.delay(1300)
        self.nextSong()
    
    def __changeMusicVolume(self, mouseX):
        self.__musicVolume = (mouseX - MusicPlayer.VOLUME_BAR_LEFT) / MusicPlayer.VOLUME_BAR_WIDTH
        pygame.mixer.music.set_volume(self.__musicVolume)
    
    def checkInput(self, mouseX, mouseY):
        if self.__previousSongButton.collides(mouseX, mouseY):
            self.__radioStationList[self.__currentPlaylistIndex][0].previousSong(self.__musicVolume)
        
        elif self.__pauseSongButton.collides(mouseX, mouseY):
            self.__radioStationList[self.__currentPlaylistIndex][0].pauseButtonAction()
        
        elif self.__nextSongButton.collides(mouseX, mouseY):
            self.__radioStationList[self.__currentPlaylistIndex][0].nextSong(self.__musicVolume)
            
        elif self.__previousRadioStationButton.collides(mouseX, mouseY):
            self.__changeRadioStations(-1)
            
        elif self.__nextRadioStationButton.collides(mouseX, mouseY):
            self.__changeRadioStations(1)
            
        elif self.__volumeBarButton.collides(mouseX, mouseY):
            self.__changeMusicVolume(mouseX)
            
    def fadeIn(self):
        temporaryVolume = pygame.mixer.music.get_volume()
        while temporaryVolume < self.__musicVolume:
            temporaryVolume += Constants.VOLUME_INCREMENT
            pygame.mixer.music.set_volume(temporaryVolume)
        pygame.mixer.music.set_volume(self.__musicVolume)
        


