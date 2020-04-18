import pygame

class Label():
    def __init__(self, top, left, width, height, backgroundColor, text, textColor, textFont, textFontSize):
        self.__topCoord = top
        self.__leftCoord = left
        self.__width = width
        self.__height = height
        self.__backgroundColor = backgroundColor
        self.__text = text
        self.__textColor = textColor
        self.__textFont = textFont
        self.__textFontSize = textFontSize
        
        self.__font = pygame.font.SysFont(self.__textFont, self.__textFontSize, True, False)
        
    def display(self, gameDisplay):
        pygame.rect.draw(gameDisplay, self.__backgroundColor, (self.__leftCoord, self.__topCoord, self.__width, self.__height))
        textBlock = self.__font.render(self.__text, True, self.__textColor)
        textRect = textBlock.get_rect()
        textRect.center = (self.__leftCoord + self.__width // 2, self.__topCoord + self.__height // 2)
        self.__gameDisplay.blit(textBlock, textRect)