class FoundImageProperty:
    def __init__(self, imageTitle):
        self.__found = False
        self.__imageTitle = imageTitle
        
    def getCompleted(self):
        return self.__found # False == 0, True == 1
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__found
    
    def updateProperty(self, imageTitle):
        if self.__imageTitle == imageTitle:
            self.__found = True