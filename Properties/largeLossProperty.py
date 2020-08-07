class LargeLossProperty:
    MINIMUM_QUANTITY = -100000
    
    def __init__(self):
        self.__largeLoss = False
        
    def getCompleted(self):
        return self.__largeLoss
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__largeLoss
    
    def updateProperty(self, losses):
        # losses = -abs(the_amount_lost)
        if losses <= LargeLossProperty.MINIMUM_QUANTITY:
            self.__largeLoss = True