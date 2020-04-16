from abc import ABC, abstractmethod

class Screen(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def setBackgroundImage(self):
        pass
    
    @abstractmethod
    def setBackgroundMusic(self):
        pass
    
    @abstractmethod
    def displayContent(self):
        pass