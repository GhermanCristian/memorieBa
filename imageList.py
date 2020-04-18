import os
from gameImage import GameImage

class ImageList:
    def __init__(self):
        self.__images = []
        self.__path = os.path.join(os.getcwd(), "Images")
        self.__loadImages()
        
    def __loadImages(self):        
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

            self.__images.append(GameImage(currentImageTitle, currentImageFullPath, currentImageSoundCue))
            
    @property
    def images(self):
        return self.__images
