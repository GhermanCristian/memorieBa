class FoundValahiaGuysProperty:
    COSTI_IMAGE_TITLE = "COSTI_1"
    TRAISTARIU_IMAGE_TITLE = "TRAISTARIU_1"
    
    def __init__(self):
        # this and the americandrim property can be generalised, by passing as parameter a list of image titles
        self.__foundCosti = False
        self.__foundTraistariu = False
        
    def getCompleted(self):
        return self.__foundCosti and self.__foundTraistariu # False == 0, True == 1
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__foundCosti and self.__foundTraistariu
    
    def updateProperty(self, imageTitle):
        if FoundValahiaGuysProperty.COSTI_IMAGE_TITLE == imageTitle:
            self.__foundCosti = True
        elif FoundValahiaGuysProperty.TRAISTARIU_IMAGE_TITLE == imageTitle:
            self.__foundTraistariu = True
