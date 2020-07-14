import os
from gameImage import GameImage

class ImageList:
    def __init__(self):
        self.__images = []
        self.__path = os.path.join(os.getcwd(), "Images")
        
        self.__specialPairs = []
        self.__matchingFirstCharacters = 10 # special_xx => 10 chararcters
        
        self.__loadImages()
        
    def __loadImages(self):
        previousImage = None
        
        soundCueList = []
        soundCuesFolder = os.path.join(os.getcwd(), "Music")
        soundCuesFolder = os.path.join(soundCuesFolder, "Sounds")
        for soundCue in os.listdir(soundCuesFolder):
            soundCueList.append(soundCue)
                
        for file in os.listdir(self.__path):
            if os.path.isdir(os.path.join(self.__path, file)):
                continue
            
            currentImageTitle = file[:-5].upper() + "_" + file[-5] #POZA_1
            currentImageFullPath = os.path.join(self.__path, file)
            currentImageSoundCue = None
            
            for soundCue in soundCueList:
                if currentImageTitle == soundCue[:-4]:
                    currentImageSoundCue = os.path.join(soundCuesFolder, soundCue)
                    break
            
            currentImage = GameImage(currentImageTitle, currentImageFullPath, currentImageSoundCue)
            self.__images.append(currentImage)
            
            if "special_" in file and previousImage != None and currentImageTitle[:self.__matchingFirstCharacters] == previousImage.title[:self.__matchingFirstCharacters]:
                self.__specialPairs.append((previousImage, currentImage))
                
            previousImage = currentImage
            
    @property
    def images(self):
        return self.__images
    
    @property
    def specialPairs(self):
        return self.__specialPairs

