class PictureSongComboProperty:
    def __init__(self, keyword):
        self.__found = False
        self.__keyword = keyword
        
    def getCompleted(self):
        return self.__found
    
    def getTotal(self):
        return 1
    
    def checkCompletion(self):
        return self.__found
    
    def foundCombo(self, pictureTitle, songTitle):
        songTitle = songTitle.upper()
        underscorePosition = pictureTitle.find('_')
        pictureTitle = pictureTitle[:underscorePosition]
        self.__found = ((self.__keyword in pictureTitle) and (pictureTitle in songTitle))