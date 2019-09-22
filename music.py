import os
import pygame
import random
from constants import INCREMENT, LOW_VOLUME, NORMAL_VOLUME

path = os.path.join(os.getcwd(), "Music")
playlist = []

for song in os.listdir(path):
    if "S_" in song:
        playlist.append(os.path.join(os.getcwd(), "Music//" + song))
        
songCount = len(playlist)
random.shuffle(playlist)
print (playlist)

def initMusic():
    pygame.mixer.init()
    pygame.mixer.music.load(playlist[0])
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.set_volume(NORMAL_VOLUME)

def playSong(crtSong):
    if crtSong == songCount - 1:
        crtSong = 0
    else:
        crtSong += 1 
    print (crtSong)  
    pygame.mixer.music.load(playlist[crtSong])
    pygame.mixer.music.play()
    
    return crtSong
    
def playSound(path, volMultiplier):
    cue = pygame.mixer.Sound(os.path.join(os.getcwd(), path))

    ch = pygame.mixer.Channel(1)
    ch.play(cue)

    pygame.mixer.music.set_volume(LOW_VOLUME)
    cue.set_volume(NORMAL_VOLUME * volMultiplier)

def fadeOut():
    vol = pygame.mixer.music.get_volume()
    while vol > 0.0:
        vol -= 3 * INCREMENT
        pygame.mixer.music.set_volume(vol)
        pygame.time.wait(50)
        
def fadeIn():
    vol = pygame.mixer.music.get_volume()
    while vol < NORMAL_VOLUME:
        vol += INCREMENT
        #print ("volume is " + str(vol))
        pygame.mixer.music.set_volume(vol)
        
