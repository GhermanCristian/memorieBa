from abc import ABC, abstractmethod

QUIT_PROGRAM = "quit"
CONTINUE_PROGRAM = "continue"

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