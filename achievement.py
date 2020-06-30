
class Achievement:
    def __init__(self, title, isSecret, description, soundCue, prop):
        self.__title = title
        self.__isSecret = isSecret
        self.__description = description
        self.__soundCue = soundCue # the path of the sound cue, the one from gameImage
        self.__property = prop
        
        self.__completed = prop.getCompleted() #these 2 are 0 by default; when they are loaded from the achievement file, they will be set to sth else
        self.__total = prop.getTotal()
        
    def setCompleted(self, newCompleted):
        self.__completed = newCompleted
        
    def setTotal(self, newTotal):
        self.__total = newTotal
        
    @property
    def title(self):
        return self.__title
    
    @property
    def completed(self):
        return self.__completed
    
    @property
    def total(self):
        return self.__total    
        
    @property
    def description(self):
        if self.__isSecret == True and self.__completed < self.__total:
            return "???"
        return self.__description
    
    @property
    def property(self):
        return self.__property
