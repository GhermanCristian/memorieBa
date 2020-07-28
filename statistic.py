class Statistic:
    def __init__(self, description, quantity, trigger, isTime):
        self.__description = description
        self.__quantity = quantity
        self.__trigger = trigger
        self.__isTime = isTime
        
    def add(self, increment):
        self.__quantity += increment    
        
    @property
    def description(self):
        return self.__description
    
    @property
    def quantity(self):
        return self.__quantity
    
    @property
    def trigger(self):
        return self.__trigger
    
    @property
    def isTime(self):
        return self.__isTime