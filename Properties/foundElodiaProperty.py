
class FoundElodiaProperty:
    ELODIA_IMAGE_TITLE = "ELODIA_1"
    
    def __init__(self):
        self.__foundElodia = False
        
    def getCompleted(self):
        return self.__foundElodia # False == 0, True == 1
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__foundElodia
    
    def updateProperty(self, imageTitle):
        if FoundElodiaProperty.ELODIA_IMAGE_TITLE == imageTitle:
            self.__foundElodia = True