class LargeLossProperty:
    MINIMUM_QUANTITY = 1000
    
    def __init__(self):
        self.__largeLoss = False
        
    def getCompleted(self):
        return self.__largeLoss
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__largeLoss
    
    def updateProperty(self, winnings):
        if winnings >= LargeLossProperty.MINIMUM_QUANTITY:
            self.__largeLoss = True