import pickle
from achievement import Achievement
from Properties.foundAllImagesProperty import FoundAllImagesProperty

class StatsRepository:
    IMAGE_FOLDER_PATH = "Images"
    
    ACHIEVEMENT_FILE_PATH = "Data//Stats//achievements.pickle"
    FOUND_ALL_IMAGES_PATH = "Data//Stats//foundAllImages.pickle"
    
    def __init__(self):
        self.__achievementList = []
        self.__loadAchievements()
    
    def __saveAchievements(self):
        file = open(StatsRepository.ACHIEVEMENT_FILE_PATH, "wb")
        pickle.dump(self.__achievementList, file)
        file.close()
    
    def __initEmptyAchievementList(self):
        foundAllImagesProperty = FoundAllImagesProperty(StatsRepository.FOUND_ALL_IMAGES_PATH, StatsRepository.IMAGE_FOLDER_PATH)
        foundAllImagesAchievement = Achievement("Pe toate ma ?", False, "Find all the images", None, foundAllImagesProperty)
        self.__achievementList.append(foundAllImagesAchievement)
        
        self.__saveAchievements()
    
    def __loadAchievements(self):
        try:
            file = open(StatsRepository.ACHIEVEMENT_FILE_PATH, "rb")
            self.__achievementList = pickle.load(file)
            file.close()
            
        except Exception:
            self.__initEmptyAchievementList()