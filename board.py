from constants import *
from imageList import ImageList
import random

class Board:
    def __init__(self):
        self.__width = BOARD_WIDTH
        self.__height = BOARD_HEIGHT
        
        self.__revealed = [] # matrix form
        self.__images = [] # matrix form
        
        self.__imageList = ImageList().images
        
        for i in range(self.__height):
            aux = []
            for j in range(self.__width):
                aux.append(False)
            self.__revealed.append(aux)
            
        for i in range(self.__height):
            aux = []
            for j in range(self.__width):
                aux.append(False)
            self.__images.append(aux)

        random.shuffle(self.__imageList)
        
    def newLevel(self, level):
        totalImages = (self.__height * self.__width) // 2 # total images in 1 level
        icons = self.__imageList[(level - 1) * totalImages : level * totalImages] * 2
        random.shuffle(icons)
        
        for i in range(self.__height):
            for j in range(self.__width):
                self.__revealed[i][j] = False
                self.__images[i][j] = icons[0]
                del icons[0]
    
    def getImage(self, i, j):
        return self.__images[i][j]
    
    def revealBox(self, i, j):
        self.__revealed[i][j] = True
        
    def coverBox(self, i, j):
        self.__revealed[i][j] = False 
    
    def isRevealed(self, i, j):
        return self.__revealed[i][j]
            
    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height