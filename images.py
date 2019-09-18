import pygame
import os
from constants import BADEA_SOUND_PATH, DUMITRESCU_SOUND_PATH, MARLANU_SOUND_PATH,\
    SILVIU_SOUND_PATH, PROSTAMOL_SOUND_PATH

path = os.path.join(os.getcwd(), "Images")
ALL_IMAGES = {}
SPECIAL_IMAGES = {}

for file in os.listdir(path):
    imageName = file[:-5].upper() + "_" + file[-5]
    if "ICON" in imageName:
        continue
    
    ALL_IMAGES[imageName] = pygame.image.load(os.path.join(path, file))
    
    if "BADEA" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = BADEA_SOUND_PATH
    if "DUMITRESCU" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = DUMITRESCU_SOUND_PATH
    if "MARLANU" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = MARLANU_SOUND_PATH
    if "SILVIU" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = SILVIU_SOUND_PATH
    if "PROSTAMOL" in imageName:
        SPECIAL_IMAGES[ ALL_IMAGES[imageName] ] = PROSTAMOL_SOUND_PATH

SERGHEI_ICON1 = pygame.image.load(os.path.join(path, "SERGHEI_ICON1.ICO"))