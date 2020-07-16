class SetNameProperty:
    def __init__(self, keywordList):
        self.__found = False
        self.__keywordList = keywordList
        
    def getCompleted(self):
        return self.__found
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__found
    
    def updateProperty(self, name): #setname
        name = name.lower()
        for keyword in self.__keywordList:
            if keyword.lower() in name:
                self.__found = True
                break