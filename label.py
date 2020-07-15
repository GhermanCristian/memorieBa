import pygame

class Label():
    def __init__(self, top, left, width, height, backgroundColor, text):
        self._topCoord = top
        self._leftCoord = left
        
        self._width = width
        if width == -1:
            self._width = len(text.content) * text.fontSize
         
        self._height = height
        self._backgroundColor = backgroundColor
        
        if (text != None):
            self._text = text.content
            self._textColor = text.color
            self._textFontName = text.fontName
            self._textFontSize = text.fontSize
            
            self._font = pygame.font.SysFont(self._textFontName, self._textFontSize, True, False)
        else:
            self._text = None
        
    def display(self, gameDisplay, thickness = -1):
        if thickness == -1:
            pygame.draw.rect(gameDisplay, self._backgroundColor, (self._leftCoord, self._topCoord, self._width, self._height))
        else:
            pygame.draw.rect(gameDisplay, self._backgroundColor, (self._leftCoord, self._topCoord, self._width, self._height), thickness)
             
        if self._text != None:
            textBlock = self._font.render(self._text, True, self._textColor)
            textRect = textBlock.get_rect()
            textRect.center = (self._leftCoord + self._width // 2, self._topCoord + self._height // 2)
            gameDisplay.blit(textBlock, textRect)