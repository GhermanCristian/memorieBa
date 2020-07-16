class BetVeteranProperty:
    TOTAL_COUNT = 2
    
    def __init__(self):
        self.__betCount = 0
        
    def getCompleted(self):
        return self.__betCount
    
    def getTotal(self):
        return BetVeteranProperty.TOTAL_COUNT
    
    def checkCompletion(self):
        return self.__betCount >= BetVeteranProperty.TOTAL_COUNT
    
    def updateProperty(self, winnings):
        self.__betCount += 1