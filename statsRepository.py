import pickle, os, achievement
from achievement import Achievement
from statistic import Statistic
from constants import Constants
from Properties.foundAllImagesProperty import FoundAllImagesProperty
from Properties.foundAllSoundCuesProperty import FoundAllSoundCuesProperty
from Properties.foundImageProperty import FoundImageProperty
from Properties.boughtFreedomProperty import BoughtFreedomProperty
from Properties.boughtTimisoreanaProperty import BoughtTimisoreanaProperty
from Properties.betVeteranProperty import BetVeteranProperty
from Properties.largeWinProperty import LargeWinProperty
from Properties.perfectLevelProperty import PerfectLevelProperty
from Properties.foundAmericandrimGuysProperty import FoundAmericandrimGuysProperty
from Properties.largeLossProperty import LargeLossProperty
from Properties.foundSpecialPairProperty import FoundSpecialPairProperty
from Properties.pictureSongComboProperty import PictureSongComboProperty
from Properties.setNameProperty import SetNameProperty
from Properties.foundValahiaGuysProperty import FoundValahiaGuysProperty

class StatsRepository:
    IMAGE_FOLDER_PATH = "Images"
    SOUND_CUE_FOLDER_NAME = os.path.join("Music", "Sounds")
    
    ACHIEVEMENT_FILE_PATH = "achievements.pickle"
    STATS_FILE_PATH = "stats.pickle"
    
    CV_IMAGE_TITLE = "CV_1"
    ELODIA_IMAGE_TITLE = "ELODIA_1"
    BECALI_ASTRONAUT_IMAGE_TITLE = "BECALI_ASTRONAUT_1"
    TARZAN_IMAGE_TITLE = "TARZAN_1"
    SILVIU_IMAGE_TITLE = "SILVIU_1"
    
    PUYA_IMAGE_TITLE = "SPECIAL_1_PUYALAFAMILIA_1"
    SISU_IMAGE_TITLE = "SPECIAL_1_SISULAFAMILIA_1"
    MARIN_IMAGE_TITLE = "SPECIAL_2_ANDREEAMARIN_1"
    BANICA_IMAGE_TITLE = "SPECIAL_2_STEFANBANICA_1"
    COSTI_IMAGE_TITLE = "SPECIAL_3_COSTIIONITA_1"
    MINUNE_IMAGE_TITLE = "SPECIAL_3_ADIMINUNE_1"
    JESUSMAN_IMAGE_TITLE = "SPECIAL_4_JESUSMAN_1"
    SCOTTY_IMAGE_TITLE = "SPECIAL_4_SCOTTY_1"
    ARNOLD_IMAGE_TITLE = "SPECIAL_5_ARNOLD_1"
    DILLON_IMAGE_TITLE = "SPECIAL_5_DILLON_1"
    IAN_IMAGE_TITLE = "SPECIAL_6_IAN_1"
    AZTECA_IMAGE_TITLE = "SPECIAL_6_AZTECA_1"
    COMAN_IMAGE_TITLE = "SPECIAL_7_COMAN_1"
    MBAPPE_IMAGE_TITLE = "SPECIAL_7_MBAPPE_1"
    FOCA_IMAGE_TITLE = "SPECIAL_8_FOCA_1"
    MO_IMAGE_TITLE = "SPECIAL_8_MO_1"
    ASAFACI_IMAGE_TITLE = "SPECIAL_9_ASAFACI_1"
    IESIACASA_IMAGE_TITLE = "SPECIAL_9_IESIACASA_1"
    
    def __init__(self):
        self.achievementList = []
        self.statsList = []
        
        self.__imageFolderPath = os.path.join(os.getcwd(), StatsRepository.IMAGE_FOLDER_PATH)
        self.__soundCueFolderPath = os.path.join(os.getcwd(), StatsRepository.SOUND_CUE_FOLDER_NAME)
        self.__achievementPath = self.__determineFilePath(StatsRepository.ACHIEVEMENT_FILE_PATH)
        self.__statsPath = self.__determineFilePath(StatsRepository.STATS_FILE_PATH)
        
        self.__loadAchievements()
        self.__loadStats()
    
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
        # as a general guideline, I should have the hidden achievements last in the list        
        self.achievementList.clear()
        self.achievementList.append(Achievement("Pe toate ma ?", False, "Find all the images", None, FoundAllImagesProperty(self.__imageFolderPath), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Ce-o zis ala ba ?", False, "Find all the sound cues", None, FoundAllSoundCuesProperty(self.__soundCueFolderPath), Constants.TRIGGER_FOUND_SOUND_CUE))
        self.achievementList.append(Achievement("You did it. You crazy son of a bitch, you did it", False, "Perfect level", None, PerfectLevelProperty(), Constants.TRIGGER_END_LEVEL))
        
        self.achievementList.append(Achievement("Bei azi, mori maine", False, "Drink Freedom", None, BoughtFreedomProperty(), Constants.TRIGGER_BOUGHT_DRINK))
        self.achievementList.append(Achievement("Alcoholic", False, "Drink Timisoreana", None, BoughtTimisoreanaProperty(), Constants.TRIGGER_BOUGHT_DRINK))
        self.achievementList.append(Achievement("Betting veteran", False, "Bet 100 times", None, BetVeteranProperty(), Constants.TRIGGER_MADE_BET))
        self.achievementList.append(Achievement("High risk, high reward", False, "Win big", None, LargeWinProperty(), Constants.TRIGGER_MADE_BET))
        self.achievementList.append(Achievement("High risk, low reward", False, "Lose big", None, LargeLossProperty(), Constants.TRIGGER_MADE_BET))
        
        self.achievementList.append(Achievement("Cioaca in libertate", True, "Find Elodia", None, FoundImageProperty(StatsRepository.ELODIA_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Somn usor", True, "Find CV", None, FoundImageProperty(StatsRepository.CV_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("One small step for a man...", True, "...one giant leap for mankind", None, FoundImageProperty(StatsRepository.BECALI_ASTRONAUT_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Buna bata", True, "Buna, Tarzan!", None, FoundImageProperty(StatsRepository.TARZAN_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("5 RON", True, "Sora-ta ce mai face ?", None, FoundImageProperty(StatsRepository.SILVIU_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        
        self.achievementList.append(Achievement("Cam atat stiu restu", True, "Americandrim", None, FoundAmericandrimGuysProperty(), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Aia importanti din Valahia", True, "Traistariu & Costi", None, FoundValahiaGuysProperty(), Constants.TRIGGER_FOUND_IMAGE))
        
        self.achievementList.append(Achievement("Tot in familie", True, "Reunite La Familia", None, FoundSpecialPairProperty(StatsRepository.PUYA_IMAGE_TITLE, StatsRepository.SISU_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Surprize, surprize", True, "Surprise Andreea Marin-Banica", None, FoundSpecialPairProperty(StatsRepository.MARIN_IMAGE_TITLE, StatsRepository.BANICA_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Of, viata mea", True, "Revolutionize the music industry", None, FoundSpecialPairProperty(StatsRepository.COSTI_IMAGE_TITLE, StatsRepository.MINUNE_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Hey Scotty", True, "Jesus, man!", None, FoundSpecialPairProperty(StatsRepository.JESUSMAN_IMAGE_TITLE, StatsRepository.SCOTTY_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Dillon!", True, "You son of a bitch!", None, FoundSpecialPairProperty(StatsRepository.ARNOLD_IMAGE_TITLE, StatsRepository.DILLON_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Baia Mare", True, "Baia Maree", None, FoundSpecialPairProperty(StatsRepository.IAN_IMAGE_TITLE, StatsRepository.AZTECA_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("200 Million", True, "Florinel Mbappe", None, FoundSpecialPairProperty(StatsRepository.COMAN_IMAGE_TITLE, StatsRepository.MBAPPE_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Ce faci F.O.C.A. ?", True, "Da bine MO, uite..", None, FoundSpecialPairProperty(StatsRepository.MO_IMAGE_TITLE, StatsRepository.FOCA_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        self.achievementList.append(Achievement("Vezi ca stiu ceva despre tine", True, "Nini ai grija!", None, FoundSpecialPairProperty(StatsRepository.ASAFACI_IMAGE_TITLE, StatsRepository.IESIACASA_IMAGE_TITLE), Constants.TRIGGER_FOUND_IMAGE))
        
        self.achievementList.append(Achievement("Zi-le Guta!", True, "Guta^2", None, PictureSongComboProperty("GUTA"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Fantastick", True, "Como bombastick", None, PictureSongComboProperty("ROMEO"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Forrrrrrza", True, "Forrrrrrza", None, PictureSongComboProperty("COSTI"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Regele Manasturului", True, "Stie tata!", None, PictureSongComboProperty("NELSON"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Freestyle tiganesc", True, "Bahoi^2", None, PictureSongComboProperty("BAHOI"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Chica Bomb", True, "Chica Bomb de la Dan Balan", None, PictureSongComboProperty("BALAN"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Nane 2008 ?", True, "Nane 2019 ?", None, PictureSongComboProperty("NANE"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("$1", True, "4 lei", None, PictureSongComboProperty("FIFTY"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Am vazut-o pe strada", True, "De ce n-ai mers la ea ?", None, PictureSongComboProperty("ZMAILI"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Eurovision 2006", True, "Tomberon", None, PictureSongComboProperty("TRAISTARIU"), Constants.TRIGGER_FOUND_COMBO))
        self.achievementList.append(Achievement("Let me live my americandrim", True, "Zice bine Puya", None, PictureSongComboProperty("PUYA"), Constants.TRIGGER_FOUND_COMBO))
        
        self.achievementList.append(Achievement("K House", True, "Usile vol. 2", None, SetNameProperty(["specii"]), Constants.TRIGGER_SET_NAME))
        self.achievementList.append(Achievement("Suntem", True, "Mr. Chinese", None, SetNameProperty(["chin", "china", "domnul"]), Constants.TRIGGER_SET_NAME))
        
        self.__saveAchievements()
    
    def __loadAchievements(self):
        try:
            file = open(self.__achievementPath, "rb")
            self.achievementList = pickle.load(file)
            file.close()
            
        except Exception:
            self.__initEmptyAchievementList()
            
    def __saveStats(self):
        file = open(self.__statsPath, "wb")
        pickle.dump(self.statsList, file)
        file.close()        
            
    def __initEmptyStatsList(self):
        self.statsList.clear()
        
        self.statsList.append(Statistic("Total picture reveals", 0, Constants.TRIGGER_REVEALED_IMAGE, False))
        self.statsList.append(Statistic("Correct guesses", 0, Constants.TRIGGER_FOUND_IMAGE, False))
        self.statsList.append(Statistic("Wrong guesses", 0, Constants.TRIGGER_FOUND_WRONG_IMAGE, False))
        self.statsList.append(Statistic("Total in-game time", 0, Constants.TRIGGER_EXIT_LEVEL, True))
        self.statsList.append(Statistic("Attempted games", 0, Constants.TRIGGER_START_GAME, False))
        self.statsList.append(Statistic("Finished games", 0, Constants.TRIGGER_FINISH_GAME, False))
        self.statsList.append(Statistic("Money earned", 0, Constants.TRIGGER_EARNED_MONEY, False))
        self.statsList.append(Statistic("Money spent", 0, Constants.TRIGGER_SPENT_MONEY, False))
        self.statsList.append(Statistic("Drinks bought", 0, Constants.TRIGGER_BOUGHT_DRINK, False))
        
        self.__saveStats()
            
    def __loadStats(self):
        try:
            file = open(self.__statsPath, "rb")
            self.statsList = pickle.load(file)
            file.close()
            
        except Exception:
            self.__initEmptyStatsList()
            
    def __satisfyAchievementProperty(self, trigger, *arguments):
        numberOfArguments = {
            Constants.TRIGGER_FOUND_IMAGE : 1,
            Constants.TRIGGER_FOUND_SOUND_CUE : 1,
            Constants.TRIGGER_BOUGHT_DRINK : 1,
            Constants.TRIGGER_MADE_BET : 1,
            Constants.TRIGGER_END_LEVEL : 0,
            Constants.TRIGGER_FOUND_COMBO : 2,
            Constants.TRIGGER_SET_NAME : 1,
        }
        
        completedAchievements = [] # finding one image can complete more than 1 achievement at a time => use a list to store all of them
        for achievement in self.achievementList:
            alreadyCompleted = achievement.prop.checkCompletion()
            if alreadyCompleted == True:
                continue
            
            if achievement.trigger == trigger:
                if numberOfArguments[trigger] == 0:
                    achievement.prop.updateProperty()
                elif numberOfArguments[trigger] == 1:
                    achievement.prop.updateProperty(arguments[0])
                elif numberOfArguments[trigger] == 2:
                    achievement.prop.updateProperty(arguments[0], arguments[1])
                
                if achievement.prop.checkCompletion():
                    completedAchievements.append(achievement)
                    
        self.__saveAchievements()
        return completedAchievements
    
    def __satisfyStatsProperty(self, trigger, increment):
        # instead of searching for a specific stat each time, I could've just memorised the position of each stat in the list
        # but that would cause issues when trying to rearrange them in the list
        for statistic in self.statsList:
            if statistic.trigger == trigger:
                statistic.add(increment)
                
        self.__saveStats()
    
    def foundImage(self, imageTitle):
        return self.__satisfyAchievementProperty(Constants.TRIGGER_FOUND_IMAGE, imageTitle)
    
    def foundSoundCue(self, soundCueTitle):
        return self.__satisfyAchievementProperty(Constants.TRIGGER_FOUND_SOUND_CUE, soundCueTitle)
    
    def boughtDrink(self, drinkType):
        return self.__satisfyAchievementProperty(Constants.TRIGGER_BOUGHT_DRINK, drinkType)
    
    def madeBet(self, winnings):
        return self.__satisfyAchievementProperty(Constants.TRIGGER_MADE_BET, winnings)
    
    def endLevel(self):
        return self.__satisfyAchievementProperty(Constants.TRIGGER_END_LEVEL)
    
    def foundCombo(self, pictureTitle, songTitle):
        return self.__satisfyAchievementProperty(Constants.TRIGGER_FOUND_COMBO, pictureTitle, songTitle)
    
    def setName(self, name):
        return self.__satisfyAchievementProperty(Constants.TRIGGER_SET_NAME, name)
    
    def foundCorrectImage(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_FOUND_IMAGE, increment)
    
    def foundWrongImage(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_FOUND_WRONG_IMAGE, increment)

    def boughtDrinkStat(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_BOUGHT_DRINK, increment)
    
    def revealedImage(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_REVEALED_IMAGE, increment)

    def exitLevel(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_EXIT_LEVEL, increment)

    def startGame(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_START_GAME, increment)
        
    def finishGame(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_FINISH_GAME, increment)
        
    def earnedMoney(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_EARNED_MONEY, increment)

    def spentMoney(self, increment):
        self.__satisfyStatsProperty(Constants.TRIGGER_SPENT_MONEY, increment)


