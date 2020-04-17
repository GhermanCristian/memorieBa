

class GameImage():
    def __init__(self, title, imageObject, soundCue = None):
        self.__title = title
        self.__imageObject = imageObject
        self.__soundCue = soundCue
        
    @property
    def title(self):
        return self.__title
    
    @property
    def imageObject(self):
        return self.__imageObject
    
    @property
    def soundCue(self):
        return self.__soundCue