import pickle, os

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
                ("Emil Boc", 155000), 
                ("e un tampit", 155010), 
                ("piperalord2000", 180000), 
                ("fifti", 200000), 
                ("connectar", 220000), 
                ("fasole", 240000), 
                ("Drake Gardescu", 260000), 
                ("slabanogu de chimita", 280000), 
                ("Kazi cu k", 300000), 
                ("Dragos Tudorache", 320000)
            ]
            
        elif "smart" in self.__filePath:
            self.scoreList = [
                ("Emil Boc", 130), 
                ("e un tampit", 131), 
                ("piperalord2000", 150), 
                ("fifti", 160), 
                ("connectar", 170), 
                ("fasole", 180), 
                ("Drake Gardescu", 190), 
                ("slabanogu de chimita", 200), 
                ("Kazi cu k", 210), 
                ("Dragos Tudorache", 220)
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
        
        
        
        