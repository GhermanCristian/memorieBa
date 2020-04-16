import pygame
import os
from constants import *

class ImageRepo:
    def __init__(self):
        self.imageList = {}
        self.imageSoundCues = {}
        
        self.__path = os.path.join(os.getcwd(), "Images")
        self.__specialPath = os.path.join(self.__path, "Special images")
        self.__loadImages()
        
        self.SERGHEI_ICON = pygame.image.load(os.path.join(self.__specialPath, "SERGHEI_ICON.ICO"))
        self.WELCOME_SCREEN = pygame.image.load(os.path.join(self.__specialPath, "WELCOME_SCREEN.jpg"))
        self.MOUSE_CURSOR = pygame.image.load(os.path.join(self.__specialPath, "MOUSE_CURSOR1.jpg"))
        self.ACE_HEARTS = pygame.image.load(os.path.join(self.__specialPath, "ACE_HEARTS.jpg"))
        self.ACE_SPADES = pygame.image.load(os.path.join(self.__specialPath, "ACE_SPADES.jpg"))
        self.SAVE_ICON = pygame.image.load(os.path.join(self.__specialPath, "SAVE_ICON.jpg"))
        self.EXIT_SCREEN_1 = pygame.image.load(os.path.join(self.__specialPath, "EXIT_SCREEN1.jpg"))
        self.EXIT_SCREEN_2 = pygame.image.load(os.path.join(self.__specialPath, "EXIT_SCREEN2.jpg"))
        
    def __loadImages(self):
        auxDict = {
            "DUMITRESCU_1": DUMITRESCU_SOUND_PATH, 
            "MARLANU": MARLANU_SOUND_PATH, 
            "SILVIU": SILVIU_SOUND_PATH, 
            "PROSTAMOL": PROSTAMOL_SOUND_PATH, 
            "BADEA_2": BADEA_SOUND_PATH, 
            "ROMEO_2": ROMEO_SOUND_PATH, 
            "GUTA_3": GUTA_SOUND_PATH, 
            "DINU_1": DINU_SOUND_PATH,
            "ZMAILI_1": ZMAILI_SOUND_PATH,
            "VELEA_1": VELEA_SOUND_PATH,
            "PITT_1": PITT_SOUND_PATH,
            "POPA": POPA_SOUND_PATH,
            "AUSTIN": AUSTIN_SOUND_PATH,
            "MARGINEANU": MARGINEANU_SOUND_PATH,
            "GEOANA": GEOANA_SOUND_PATH, 
            "DESPOT": DESPOT_SOUND_PATH,
            "BORCEA": BORCEA_SOUND_PATH,
            "DRAGONU": PRA_SOUND_PATH,
            "JACKSON": JACKSON_SOUND_PATH,
            "ROBY": ROBY_SOUND_PATH,
            "BIJU": BIJU_SOUND_PATH,
            "BRET": BRET_SOUND_PATH,
            "STEINER": STEINER_SOUND_PATH,
            "HAGI_1": HAGI_SOUND_PATH,
            "IOHANNIS": IOHANNIS_SOUND_PATH,
            "GARCEA": GARCEA_SOUND_PATH,
            "BECALI_3": BECALI_SOUND_PATH,
            "HOGAN_2": HOGAN_SOUND_PATH,
            "METICUZOLITATE": METICUZOLITATE_SOUND_PATH
        }
        
        for file in os.listdir(self.__path):
            if os.path.isdir(os.path.join(self.__path, file)):
                continue
            
            imageName = file[:-5].upper() + "_" + file[-5]
            
            self.imageList[imageName] = pygame.image.load(os.path.join(self.__path, file))
            for name in auxDict.keys():
                if name in imageName:
                    self.imageSoundCues[ self.imageList[imageName] ] = auxDict[name]
                    break


