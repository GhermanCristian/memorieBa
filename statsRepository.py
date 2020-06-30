import pickle
from achievement import Achievement
from Properties.foundAllImagesProperty import FoundAllImagesProperty
import os
import achievement

class StatsRepository:
    IMAGE_FOLDER_PATH = "Images"
    
    ACHIEVEMENT_FILE_PATH = "achievements.pickle"
    FOUND_ALL_IMAGES_PATH = "foundAllImages.pickle"
    
    def __init__(self):
        self.achievementList = []
        
        self.__imageFolderPath = os.path.join(os.getcwd(), "Images")
        self.__achievementPath = self.__determineFilePath(StatsRepository.ACHIEVEMENT_FILE_PATH)
        self.__foundAllImagesPath = self.__determineFilePath(StatsRepository.FOUND_ALL_IMAGES_PATH)
        
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
        foundAllImagesProperty = FoundAllImagesProperty(self.__foundAllImagesPath, self.__imageFolderPath)
        foundAllImagesAchievement = Achievement("Pe toate ma ?", False, "Find all the images", None, foundAllImagesProperty, Achievement.TRIGGER_FOUND_ALL_IMAGES)
        self.achievementList.append(foundAllImagesAchievement)
        
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
        completedAchievements = []
        for achievement in self.achievementList:
            if achievement.trigger == Achievement.TRIGGER_FOUND_ALL_IMAGES:
                achievement.prop.foundImage(imageTitle)
                if achievement.prop.checkCompletion():
                    completedAchievements.append(achievement)
        self.__saveAchievements()
        return completedAchievements
    
    
    
    
