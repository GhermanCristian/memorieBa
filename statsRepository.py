import pickle
from achievement import Achievement
from Properties.foundAllImagesProperty import FoundAllImagesProperty
from Properties.foundAllSoundCuesProperty import FoundAllSoundCuesProperty
from Properties.foundCVProperty import FoundCVProperty
import os
import achievement
from Properties.foundElodiaProperty import FoundElodiaProperty

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
        foundAllImagesProperty = FoundAllImagesProperty(self.__imageFolderPath)
        foundAllImagesAchievement = Achievement("Pe toate ma ?", False, "Find all the images", None, foundAllImagesProperty, Achievement.TRIGGER_FOUND_IMAGE)
        self.achievementList.append(foundAllImagesAchievement)
        
        foundAllSoundCuesProperty = FoundAllSoundCuesProperty(self.__soundCueFolderPath)
        foundAllSoundCuesAchievement = Achievement("Ce-o zis ala ba ?", False, "Find all the sound cues", None, foundAllSoundCuesProperty, Achievement.TRIGGER_FOUND_SOUND_CUE)
        self.achievementList.append(foundAllSoundCuesAchievement)
        
        foundElodiaProperty = FoundElodiaProperty()
        foundElodiaAchievement = Achievement("Cioaca in libertate", True, "Find Elodia", None, foundElodiaProperty, Achievement.TRIGGER_FOUND_IMAGE)
        self.achievementList.append(foundElodiaAchievement)
        
        foundCVProperty = FoundCVProperty()
        foundCVAchievement = Achievement("Somn usor", True, "Find CV", None, foundCVProperty, Achievement.TRIGGER_FOUND_IMAGE)
        self.achievementList.append(foundCVAchievement)
        
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
    
    
    
    
