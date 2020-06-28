from imageList import ImageList
import random

class Board:
    BOARD_WIDTH = 6
    BOARD_HEIGHT = 5
    
    def __init__(self):
        self.__width = Board.BOARD_WIDTH
        self.__height = Board.BOARD_HEIGHT
        
        self.__revealed = [] # matrix form
        self.__images = [] # matrix form
        
        self.__imageListObject = ImageList()
        self.__imageList = self.__imageListObject.images
        
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
        
        self.__specialPairs = self.__imageListObject.specialPairs
        
    def newLevel(self, level):
        icons = []
        totalImages = (self.__height * self.__width) // 2 # total images in 1 level
        
        for index in range((level - 1) * totalImages, level * totalImages):
            foundSpecialPair = False

            for specialPair in self.__specialPairs:
                if self.__imageList[index].title == specialPair[0].title or self.__imageList[index].title == specialPair[1].title:
                    icons.append(specialPair[0])
                    icons.append(specialPair[1])
                    foundSpecialPair = True

                    # remove the "opposite" image
                    if self.__imageList[index].title == specialPair[0].title:
                        self.__imageList.remove(specialPair[1])
                    else:
                        self.__imageList.remove(specialPair[0])
                    break
                
            if foundSpecialPair == False:
                icons.append(self.__imageList[index])
                icons.append(self.__imageList[index])
        
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
    
    @property
    def specialPairs(self):
        return self.__specialPairs