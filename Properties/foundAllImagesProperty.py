import os
import pickle

class FoundAllImagesProperty:
    def __init__(self, picklePath, imageFolder):
        self.__picklePath = picklePath
        self.__imageFolder = imageFolder
        self.__imagesDict = {}
        self.__loadPickle()
        # the dict will be loaded with pairs (img, state), where state is a boolean (true = image has been found already)

    def __initEmpty(self):
        for file in os.listdir(self.__imageFolder):
            if os.path.isdir(os.path.join(self.__path, file)):
                continue
            currentImageTitle = file[:-5].upper() + "_" + file[-5] #POZA_1
            self.__imagesDict[currentImageTitle] = False
        self.__savePickle()

    def __savePickle(self):
        file = open(self.__filePath, "wb")
        pickle.dump(self.scoreList, file)
        file.close()

    def __loadPickle(self):
        try:
            file = open(self.__picklePath, "rb")
            self.__imagesDict = pickle.load(file)
            file.close()
            
        except Exception:
            self.__initEmpty()

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
        self.__savePickle()
