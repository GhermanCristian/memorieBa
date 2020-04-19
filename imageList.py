import os
from gameImage import GameImage

class ImageList:
    def __init__(self):
        self.__images = []
        self.__path = os.path.join(os.getcwd(), "Images")
        
        self.specialPairs = []
        self.__matchingFirstCharacters = 10
        
        self.__loadImages()
        
    def __loadImages(self):
        previousImage = None
                
        for file in os.listdir(self.__path):
            if os.path.isdir(os.path.join(self.__path, file)):
                continue
            
            currentImageTitle = file[:-5].upper() + "_" + file[-5] #POZA_1
            currentImageFullPath = os.path.join(self.__path, file)
            currentImageSoundCue = None
            
            soundCuesFolder = os.path.join(os.getcwd(), "Music")
            for soundCue in os.listdir(soundCuesFolder):
                if currentImageTitle == soundCue[:-4]:
                    currentImageSoundCue = os.path.join("Music", soundCue)
                    break
            
            currentImage = GameImage(currentImageTitle, currentImageFullPath, currentImageSoundCue)
            self.__images.append(currentImage)
            
            if "special_" in file and previousImage != None and currentImageTitle[:self.__matchingFirstCharacters] == previousImage.title[:self.__matchingFirstCharacters]:
                self.specialPairs.append((previousImage, currentImage))
                print (previousImage.title)
                print (currentImage.title)
                
            previousImage = currentImage
            
    @property
    def images(self):
        return self.__images

