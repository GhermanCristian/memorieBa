import pickle
import os

class Leaderboard:
    ENTRIES_COUNT = 10
    
    def __init__(self, filePath):
        self.scoreList = []
        self.__filePath = os.path.join(os.getcwd(), "Data")
        self.__filePath = os.path.join(self.__filePath, "Leaderboards")
        self.__filePath = os.path.join(self.__filePath, filePath)
        
        self.__loadPickle()
    
    def __initEmptyPickle(self):
        if "fast" in self.__filePath:
            self.scoreList = [
                ("Emil Boc", 170000), 
                ("e un tampit", 170010), 
                ("piperalord2000", 200000), 
                ("fifti", 220000), 
                ("connectar", 240000), 
                ("fasole", 260000), 
                ("Drake Gardescu", 280000), 
                ("slabanogu de chimita", 300000), 
                ("Kazi cu k", 320000), 
                ("Dragos Tudorache", 340000)
            ]
            
        elif "smart" in self.__filePath:
            self.scoreList = [
                ("Emil Boc", 140), 
                ("e un tampit", 141), 
                ("piperalord2000", 165), 
                ("fifti", 200), 
                ("connectar", 225), 
                ("fasole", 250), 
                ("Drake Gardescu", 275), 
                ("slabanogu de chimita", 300), 
                ("Kazi cu k", 325), 
                ("Dragos Tudorache", 350)
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
        
        
        
        