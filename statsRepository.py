import pickle, os, achievement
from achievement import Achievement
from Properties.foundAllImagesProperty import FoundAllImagesProperty
from Properties.foundAllSoundCuesProperty import FoundAllSoundCuesProperty
from Properties.foundCVProperty import FoundCVProperty
from Properties.foundElodiaProperty import FoundElodiaProperty
from Properties.boughtFreedomProperty import BoughtFreedomProperty
from Properties.boughtTimisoreanaProperty import BoughtTimisoreanaProperty
from Properties.betVeteranProperty import BetVeteranProperty
from Properties.largeWinProperty import LargeWinProperty
from Properties.perfectLevelProperty import PerfectLevelProperty
from Properties.foundAmericandrimGuysProperty import FoundAmericandrimGuysProperty
from Properties.largeLossProperty import LargeLossProperty
from Properties.foundLaFamiliaProperty import FoundLaFamiliaProperty

class StatsRepository:
    IMAGE_FOLDER_PATH = "Images"
    SOUND_CUE_FOLDER_NAME = "Music"
    
    ACHIEVEMENT_FILE_PATH = "achievements.pickle"
    
    def __init__(self):
        self.achievementList = []
        
        self.__imageFolderPath = os.path.join(os.getcwd(), StatsRepository.IMAGE_FOLDER_PATH)
        self.__soundCueFolderPath = os.path.join(os.getcwd(), StatsRepository.SOUND_CUE_FOLDER_NAME)
        self.__achievementPath = self.__determineFilePath(StatsRepository.ACHIEVEMENT_FILE_PATH)
        
        self.__loadAchievements()
    
    def __determineFilePath(self, filename):
        path = os.path.join(os.getcwd(), "Data")
        path = os.path.join(path, "Stats")
        path = os.path.join(path, filename)
        return path 
    
    def __saveAchievements(self):
        file = open(self.__achievementPath, "wb")
        pickle.dump(self.achievementList, file)
        file.close()
    
    def __initEmptyAchievementList(self):        
        auxAchievementList = [
            Achievement("Pe toate ma ?", False, "Find all the images", None, FoundAllImagesProperty(self.__imageFolderPath), Achievement.TRIGGER_FOUND_IMAGE),
            Achievement("Ce-o zis ala ba ?", False, "Find all the sound cues", None, FoundAllSoundCuesProperty(self.__soundCueFolderPath), Achievement.TRIGGER_FOUND_SOUND_CUE),
            Achievement("Cioaca in libertate", True, "Find Elodia", None, FoundElodiaProperty(), Achievement.TRIGGER_FOUND_IMAGE),
            Achievement("Somn usor", True, "Find CV", None, FoundCVProperty(), Achievement.TRIGGER_FOUND_IMAGE),
            Achievement("Bei azi, mori maine", False, "Drink Freedom", None, BoughtFreedomProperty(), Achievement.TRIGGER_BOUGHT_DRINK),
            Achievement("Alcoholic", False, "Drink Timisoreana", None, BoughtTimisoreanaProperty(), Achievement.TRIGGER_BOUGHT_DRINK),
            Achievement("Betting veteran", False, "Bet 100 times", None, BetVeteranProperty(), Achievement.TRIGGER_MADE_BET),
            Achievement("High risk, high reward", False, "Win big", None, LargeWinProperty(), Achievement.TRIGGER_MADE_BET),
            Achievement("High risk, low reward", False, "Lose big", None, LargeLossProperty(), Achievement.TRIGGER_MADE_BET),
            Achievement("You did it. You crazy son of a bitch, you did it", False, "Perfect level", None, PerfectLevelProperty(), Achievement.TRIGGER_END_LEVEL),
            Achievement("Cam atat stiu restu", True, "Americandrim", None, FoundAmericandrimGuysProperty(), Achievement.TRIGGER_FOUND_IMAGE),
            Achievement("Tot in familie", True, "Reunite La Familia", None, FoundLaFamiliaProperty(), Achievement.TRIGGER_FOUND_IMAGE),
        ]
        
        self.achievementList.clear()
        self.achievementList.extend(auxAchievementList)
        
        self.__saveAchievements()
    
    def __loadAchievements(self):
        try:
            file = open(self.__achievementPath, "rb")
            self.achievementList = pickle.load(file)
            file.close()
            
        except Exception:
            self.__initEmptyAchievementList()
            
    def foundImage(self, imageTitle):
        #this can probably be generalized
        completedAchievements = [] # finding one image can complete more than 1 achievement at a time => use a list to store all of them
        for achievement in self.achievementList:
            alreadyCompleted = achievement.prop.checkCompletion()
            if alreadyCompleted == True:
                continue
            
            if achievement.trigger == Achievement.TRIGGER_FOUND_IMAGE:
                achievement.prop.foundImage(imageTitle)
                if achievement.prop.checkCompletion():
                    completedAchievements.append(achievement)
                    
        self.__saveAchievements()
        return completedAchievements
    
    def foundSoundCue(self, soundCueTitle):
        completedAchievements = []
        for achievement in self.achievementList:
            alreadyCompleted = achievement.prop.checkCompletion()
            if alreadyCompleted == True:
                continue
            
            if achievement.trigger == Achievement.TRIGGER_FOUND_SOUND_CUE:
                achievement.prop.foundSoundCue(soundCueTitle)
                if achievement.prop.checkCompletion():
                    completedAchievements.append(achievement)
                    
        self.__saveAchievements()
        return completedAchievements
    
    def boughtDrink(self, drinkType):
        completedAchievements = []
        for achievement in self.achievementList:
            alreadyCompleted = achievement.prop.checkCompletion()
            if alreadyCompleted == True:
                continue
            
            if achievement.trigger == Achievement.TRIGGER_BOUGHT_DRINK:
                achievement.prop.boughtDrink(drinkType)
                if achievement.prop.checkCompletion():
                    completedAchievements.append(achievement)
                    
        self.__saveAchievements()
        return completedAchievements
    
    def madeBet(self, winnings):
        completedAchievements = []
        for achievement in self.achievementList:
            alreadyCompleted = achievement.prop.checkCompletion()
            if alreadyCompleted == True:
                continue
            
            if achievement.trigger == Achievement.TRIGGER_MADE_BET:
                achievement.prop.madeBet(winnings)
                if achievement.prop.checkCompletion():
                    completedAchievements.append(achievement)
                    
        self.__saveAchievements()
        return completedAchievements
    
    def endLevel(self):
        completedAchievements = []
        for achievement in self.achievementList:
            alreadyCompleted = achievement.prop.checkCompletion()
            if alreadyCompleted == True:
                continue
            
            if achievement.trigger == Achievement.TRIGGER_END_LEVEL:
                achievement.prop.endLevel()
                if achievement.prop.checkCompletion():
                    completedAchievements.append(achievement)
                    
        self.__saveAchievements()
        return completedAchievements
    
    
