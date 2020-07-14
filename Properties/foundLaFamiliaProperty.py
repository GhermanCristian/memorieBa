class FoundLaFamiliaProperty:
    PUYA_IMAGE_TITLE = "SPECIAL_1_PUYALAFAMILIA_1"
    SISU_IMAGE_TITLE = "SPECIAL_1_SISULAFAMILIA_1"
    
    def __init__(self):
        self.__foundPuya = False
        self.__foundSisu = False
        self.__isCompleted = False
        
    def getCompleted(self):
        return self.__isCompleted # False == 0, True == 1
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__isCompleted
    
    def foundImage(self, imageTitle):
        if FoundLaFamiliaProperty.PUYA_IMAGE_TITLE == imageTitle:
            if self.__foundPuya == True: # if this picture was already found => we got the same special picture twice => reset everything
                self.__foundPuya = self.__foundSisu = False
            else:
                self.__foundPuya = True
                if self.__foundSisu == True:
                    self.__isCompleted = True
                
        elif FoundLaFamiliaProperty.SISU_IMAGE_TITLE == imageTitle:
            if self.__foundSisu == True: # if this picture was already found => we got the same special picture twice => reset everything
                self.__foundPuya = self.__foundSisu = False
            else:
                self.__foundSisu = True
                if self.__foundPuya == True:
                    self.__isCompleted = True
                
        elif self.__isCompleted == False: # when any picture but these special ones is found => reset everything
            self.__foundPuya = self.__foundSisu = False