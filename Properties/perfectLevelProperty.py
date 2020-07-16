class PerfectLevelProperty:
    def __init__(self):
        self.__isPerfect = False
        
    def getCompleted(self):
        return self.__isPerfect
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__isPerfect
    
    def updateProperty(self):
        self.__isPerfect = True