import pygame
import os
from constants import *

path = os.path.join(os.getcwd(), "Images")
ALL_IMAGES = {}
SPECIAL_IMAGES = {}

for file in os.listdir(path):
    imageName = file[:-5].upper() + "_" + file[-5]
    if "ICON" in imageName:
        continue
    
    ALL_IMAGES[imageName] = pygame.image.load(os.path.join(path, file))
    
    if "DUMITRESCU" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = DUMITRESCU_SOUND_PATH
    elif "MARLANU" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = MARLANU_SOUND_PATH
    elif "SILVIU" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = SILVIU_SOUND_PATH
    elif "PROSTAMOL" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = PROSTAMOL_SOUND_PATH
    elif imageName == "BADEA_2":
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = BADEA_SOUND_PATH
    elif imageName == "ROMEO_2":
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = ROMEO_SOUND_PATH
    #elif "JEREMY" in imageName:
        #SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = JEREMY_SOUND_PATH
    elif imageName == "GUTA_3":
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = GUTA_SOUND_PATH

SERGHEI_ICON1 = pygame.image.load(os.path.join(path, "SERGHEI_ICON1.ICO"))