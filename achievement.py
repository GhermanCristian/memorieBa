class Achievement:
    # To add a new achievement to the game
    # 0. Delete the achievement file in Stats (a new one will be created next time the program is run)
    # 1. Here, define its "trigger" - codename for the function that will update its property
        # A trigger may be used for more than 1 property - so you don't always have to create a new trigger
    # 2. In the screen where the achievement is checked, in __processAchievement, add the function and its no of args to the numberOfArguments dict
        # Multiple properties might share the same function, so you don't always have to create and add a new one
        # Also call the __processAchievement function wherever in the code it is required
    # 3. In statsRepository, in initEmptyAchievementList, create a new property + achievement and add them to the achievementList
    # 4. In statsRepository, create a new function, which will be called from a screen to update a certain property based on the trigger
    
    def __init__(self, title, isSecret, description, soundCue, prop, trigger):
        self.__title = title
        self.__isSecret = isSecret
        self.__description = description
        self.__soundCue = soundCue # the path of the sound cue, the one from gameImage
        self.__prop = prop # property, but I cannot use that word because it's reserved
        self.__trigger = trigger # the name of the function that will trigger an update in the property
        
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
        if self.__isSecret == True and self.completed < self.total:
            return "???"
        return self.__description
    
    @property
    def prop(self):
        return self.__prop
    
    @property
    def trigger(self):
        return self.__trigger
