from label import Label
import pygame

class Button(Label):
    def __init__(self, top, left, width, height, backgroundColor, text):
        Label.__init__(self, top, left, width, height, backgroundColor, text)
        
    def collides(self, x, y):
        return (self._leftCoord <= x <= self._leftCoord + self._width and self._topCoord <= y <= self._topCoord + self._height)
    
    def drawHighlight(self, gameDisplay, highlightColor, highlightBorderSize):
        pygame.draw.rect(gameDisplay, highlightColor, (self._leftCoord - highlightBorderSize, self._topCoord - highlightBorderSize, self._width + 2 * highlightBorderSize, self._height + 2 * highlightBorderSize), highlightBorderSize)