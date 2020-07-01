class Achievement:
    TRIGGER_FOUND_ALL_IMAGES = "foundAllImages"
    
    def __init__(self, title, isSecret, description, soundCue, prop, trigger):
        self.__title = title
        self.__isSecret = isSecret
        self.__description = description
        self.__soundCue = soundCue # the path of the sound cue, the one from gameImage
        self.__prop = prop # property, but I cannot use that word because it's reserved
        self.__trigger = trigger # the function that will trigger an update in the property
        
        self.__completed = prop.getCompleted()
        self.__total = prop.getTotal()
        
    def setCompleted(self, newCompleted):
        self.__completed = newCompleted
        
    def setTotal(self, newTotal):
        self.__total = newTotal
        
    @property
    def title(self):
        return self.__title
    
    @property
    def isSecret(self):
        return self.__isSecret
    
    @property
    def completed(self):
        return self.__prop.getCompleted()
    
    @property
    def total(self):
        return self.__prop.getTotal()   
        
    @property
    def description(self):
        if self.__isSecret == True and self.__completed < self.__total:
            return "???"
        return self.__description
    
    @property
    def prop(self):
        return self.__prop
    
    @property
    def trigger(self):
        return self.__trigger
