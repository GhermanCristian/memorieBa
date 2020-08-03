import pygame

class Text():
    def __init__(self, content, fontName, fontSize, color, isItalic = False):
        self.__content = content
        self.__fontName = fontName
        self.__fontSize = fontSize
        self.__color = color
        
        try:
            self.__font = pygame.font.SysFont(self.__fontName, self.__fontSize, True, isItalic)
        except: # apparently some fonts don't have both bold and italic available
            self.__font = pygame.font.SysFont(self.__fontName, self.__fontSize, True, False)
    
    def display(self, gameDisplay, topCoord, leftCoord):
        gameDisplay.blit(self.__font.render(self.__content, True, self.__color, None), (leftCoord, topCoord))
        
    @property
    def content(self):
        return self.__content
    
    @property
    def fontName(self):
        return self.__fontName
    
    @property
    def fontSize(self):
        return self.__fontSize
    
    @property
    def color(self):
        return self.__color
    
    @property
    def font(self):
        return self.__font