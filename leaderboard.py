import pickle
import os

class Leaderboard:
    ENTRIES_COUNT = 10
    
    def __init__(self, filePath):
        self.scoreList = []
        self.__filePath = os.path.join(os.getcwd(), "Leaderboards")
        self.__filePath = os.path.join(self.__filePath, filePath)
        
        self.__loadPickle()
    
    def __initEmptyPickle(self):
        if "fast" in self.__filePath:
            self.scoreList = [
                ("Emil Boc", 400000), 
                ("e un tampit", 400010), 
                ("piperalord2000", 500000), 
                ("fifti", 600000), 
                ("connectar", 750000), 
                ("fasole", 800000), 
                ("Drake Gardescu", 850000), 
                ("slabanogu de chimita", 900000), 
                ("Kazi cu k", 950000), 
                ("Dragos Tudorache", 1000000)
            ]
            
        elif "smart" in self.__filePath:
            self.scoreList = [
                ("Emil Boc", 200), 
                ("e un tampit", 201), 
                ("piperalord2000", 275), 
                ("fifti", 300), 
                ("connectar", 325), 
                ("fasole", 350), 
                ("Drake Gardescu", 375), 
                ("slabanogu de chimita", 400), 
                ("Kazi cu k", 425), 
                ("Dragos Tudorache", 450)
            ]
            
        self.__savePickle()
    
    # reads the list from the pickle
    def __loadPickle(self):
        try:
            file = open(self.__filePath, "rb")
            self.scoreList = pickle.load(file)
            file.close()
            
        except Exception:
            self.__initEmptyPickle()
            
    # writes a list to the pickle
    def __savePickle(self):
        file = open(self.__filePath, "wb")
        pickle.dump(self.scoreList, file)
        file.close()
        
    def checkResult(self, result):
        self.__loadPickle()
        return (result <= self.scoreList[Leaderboard.ENTRIES_COUNT - 1][1])
        
    def addResult(self, result, name):
        index = Leaderboard.ENTRIES_COUNT - 1
        
        while index >= 0 and result <= self.scoreList[index][1]:
            index -= 1
            
        self.scoreList.insert(index + 1, (name, result))
        self.scoreList.pop() 
        self.__savePickle()
        
        
        
        