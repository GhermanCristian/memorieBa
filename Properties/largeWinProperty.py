class LargeWinProperty:
    MINIMUM_QUANTITY = 100000
    
    def __init__(self):
        self.__largeWin = False
        
    def getCompleted(self):
        return self.__largeWin
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__largeWin
    
    def updateProperty(self, winnings):
        if winnings >= LargeWinProperty.MINIMUM_QUANTITY:
            self.__largeWin = True