class BoughtFreedomProperty:
    TOTAL_COUNT = 100
    
    def __init__(self):
        self.__drinkCount = 0
        
    def getCompleted(self):
        return self.__drinkCount
    
    def getTotal(self):
        return BoughtFreedomProperty.TOTAL_COUNT
    
    def checkCompletion(self):
        return self.__drinkCount >= BoughtFreedomProperty.TOTAL_COUNT
    
    def updateProperty(self, drinkType):
        if drinkType == "freedom":
            self.__drinkCount += 1