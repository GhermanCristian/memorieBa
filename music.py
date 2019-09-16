import os
import pygame
import random
from constants import INCREMENT, LOW_VOLUME, NORMAL_VOLUME

def playMusic():
    song = os.path.join(os.getcwd(), "Music//BALKANI.ogg")
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1, random.randint(0, 250))
    pygame.mixer.music.set_volume(LOW_VOLUME)
    
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
        
