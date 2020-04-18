from label import Label
import pygame

class Button(Label):
    def __init__(self, top, left, width, height, backgroundColor, text, textColor, textFont, textFontSize):
        Label.__init__(self, top, left, width, height, backgroundColor, text, textColor, textFont, textFontSize)
        
    def collides(self, x, y):
        return (self.__leftCoord <= x <= self.__leftCoord + self.__width and self.__topCoord <= y <= self.__topCoord + self.__height)
    
    def drawHighlight(self, highlightColor, highlightBorderSize):
        pygame.draw.rect(self.__gameDisplay, highlightColor, (self.__leftCoord - highlightBorderSize, self.__topCoord - highlightBorderSize, self.__width + 2 * highlightBorderSize, self.__height + 2 * highlightBorderSize), highlightBorderSize)