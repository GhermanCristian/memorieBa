class FoundAmericandrimGuysProperty:
    NADIA_IMAGE_TITLE = "NADIA_1"
    TIRIAC_IMAGE_TITLE = "TIRIAC_1"
    CEAUSESCU_IMAGE_TITLE = "CEASCA_1"
    HAGI_IMAGE_TITLE = "HAGI_2"
    
    def __init__(self):
        self.__foundNadia = False
        self.__foundTiriac = False
        self.__foundCeausescu = False
        self.__foundHagi = False
        
    def getCompleted(self):
        return self.__foundNadia and self.__foundTiriac and self.__foundCeausescu and self.__foundHagi # False == 0, True == 1
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__foundNadia and self.__foundTiriac and self.__foundCeausescu and self.__foundHagi
    
    def updateProperty(self, imageTitle):
        if FoundAmericandrimGuysProperty.NADIA_IMAGE_TITLE == imageTitle:
            self.__foundNadia = True
        elif FoundAmericandrimGuysProperty.TIRIAC_IMAGE_TITLE == imageTitle:
            self.__foundTiriac = True
        elif FoundAmericandrimGuysProperty.CEAUSESCU_IMAGE_TITLE == imageTitle:
            self.__foundCeausescu = True
        elif FoundAmericandrimGuysProperty.HAGI_IMAGE_TITLE == imageTitle:
            self.__foundHagi = True