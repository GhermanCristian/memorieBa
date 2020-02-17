import pygame
import os
from constants import *

class ImageRepo:
    def __init__(self):
        self.imageList = {}
        self.imageSoundCues = {}
        
        self.__path = os.path.join(os.getcwd(), "Images")
        self.__loadImages()
        
        self.SERGHEI_ICON1 = pygame.image.load(os.path.join(self.__path, "SERGHEI_ICON1.ICO"))
        self.WELCOME_SCREEN = pygame.image.load(os.path.join(self.__path, "WELCOME_SCREEN2.jpg"))
        
    def __loadImages(self):
        auxDict = {
            "DUMITRESCU": DUMITRESCU_SOUND_PATH, 
            "MARLANU": MARLANU_SOUND_PATH, 
            "SILVIU": SILVIU_SOUND_PATH, 
            "PROSTAMOL": PROSTAMOL_SOUND_PATH, 
            "BADEA_2": BADEA_SOUND_PATH, 
            "ROMEO_2": ROMEO_SOUND_PATH, 
            "GUTA_3": GUTA_SOUND_PATH, 
            "DINU_1": DINU_SOUND_PATH
        }
        
        for file in os.listdir(self.__path):
            imageName = file[:-5].upper() + "_" + file[-5]
            if "ICON" in imageName or "SCREEN" in imageName:
                continue
            
            self.imageList[imageName] = pygame.image.load(os.path.join(self.__path, file))
            for name in auxDict.keys():
                if name in imageName:
                    self.imageSoundCues[ self.imageList[imageName] ] = auxDict[name]
                    break
