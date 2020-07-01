import os

class FoundAllSoundCuesProperty:
    def __init__(self, soundCueFolder):
        self.__soundCueFolder = soundCueFolder
        self.__soundCuesDict = {}
        self.__initEmptyProperty()

    def __initEmptyProperty(self):
        for file in os.listdir(self.__soundCueFolder):
            if os.path.isdir(os.path.join(self.__soundCueFolder, file)):
                continue
            
            currentSoundCue = os.path.join(self.__soundCueFolder, file)
            self.__soundCuesDict[currentSoundCue] = False

    def getCompleted(self):
        count = 0
        for status in self.__soundCuesDict.values():
            if status == True:
                count += 1
        return count
    
    def getTotal(self):
        return len(self.__soundCuesDict)

    def checkCompletion(self):
        return self.getCompleted() == self.getTotal()

    def foundSoundCue(self, soundCueTitle):
        self.__soundCuesDict[soundCueTitle] = True