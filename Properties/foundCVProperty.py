
class FoundCVProperty:
    CV_IMAGE_TITLE = "CV_1"
    
    def __init__(self):
        self.__foundCV = False
        
    def getCompleted(self):
        return self.__foundCV # False == 0, True == 1
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__foundCV
    
    def foundImage(self, imageTitle):
        if FoundCVProperty.CV_IMAGE_TITLE == imageTitle:
            self.__foundCV = True