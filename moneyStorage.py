import os
import pickle

class MoneyStorage():
    def __init__(self):
        self.__filePath = os.path.join(os.getcwd(), "Data")
        self.__filePath = os.path.join(self.__filePath, "moneySum.pickle")
    
    def __initEmptyPickle(self):
        self.saveMoney(100000.0);
    
    def saveMoney(self, moneyQuantity):
        file = open(self.__filePath, "wb")
        pickle.dump(moneyQuantity, file)
        file.close()
    
    def loadMoney(self):
        moneyQuantity = 100000.0
        
        try:
            file = open(self.__filePath, "rb")
            moneyQuantity = pickle.load(file)
            file.close()
            
        except Exception:
            self.__initEmptyPickle()
            
        return moneyQuantity