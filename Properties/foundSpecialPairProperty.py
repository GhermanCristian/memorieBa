class FoundSpecialPairProperty:
    def __init__(self, firstImageTitle, secondImageTitle):
        self.__foundFirst = False
        self.__foundSecond = False
        self.__isCompleted = False
        
        self.__firstImageTitle = firstImageTitle
        self.__secondImageTitle = secondImageTitle
        
    def getCompleted(self):
        return self.__isCompleted # False == 0, True == 1
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__isCompleted
    
    def foundImage(self, imageTitle):
        if self.__firstImageTitle == imageTitle:
            if self.__foundFirst == True: # if this picture was already found => we got the same special picture twice => reset everything
                self.__foundFirst = self.__foundSecond = False
            else:
                self.__foundFirst = True
                if self.__foundSecond == True:
                    self.__isCompleted = True
                
        elif self.__secondImageTitle == imageTitle:
            if self.__foundSecond == True: # if this picture was already found => we got the same special picture twice => reset everything
                self.__foundFirst = self.__foundSecond = False
            else:
                self.__foundSecond = True
                if self.__foundFirst == True:
                    self.__isCompleted = True
                
        elif self.__isCompleted == False: # when any picture but these special ones is found => reset everything
            self.__foundFirst = self.__foundSecond = False