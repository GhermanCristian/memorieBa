import os

class FoundAllImagesProperty:
    def __init__(self, imageFolder):
        self.__imageFolder = imageFolder
        self.__imagesDict = {}
        self.__initEmptyProperty()

    def __initEmptyProperty(self):
        for file in os.listdir(self.__imageFolder):
            if os.path.isdir(os.path.join(self.__imageFolder, file)):
                continue
            
            currentImageTitle = file[:-5].upper() + "_" + file[-5] #POZA_1
            self.__imagesDict[currentImageTitle] = False

    def getCompleted(self):
        count = 0
        for status in self.__imagesDict.values():
            if status == True:
                count += 1
        return count
    
    def getTotal(self):
        return len(self.__imagesDict)

    def checkCompletion(self):
        return self.getCompleted() == self.getTotal()

    def foundImage(self, imageTitle):
        self.__imagesDict[imageTitle] = True
        

