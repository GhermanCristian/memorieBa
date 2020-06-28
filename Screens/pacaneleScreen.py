from Screens.screen import Screen
import pygame
import os
import random
from constants import Constants
from song import Song
from text import Text
from label import Label
from button import Button
from pygame.constants import QUIT, MOUSEMOTION, K_ESCAPE, KEYUP, MOUSEBUTTONUP

class PacaneleScreen(Screen):
    ACE_OF_SPADES_IMAGE = "ACE_SPADES.jpg"
    ACE_OF_HEARTS_IMAGE = "ACE_HEARTS.jpg"
    SAVE_ICON_IMAGE = "SAVE_ICON.jpg"
    BILL_1_RON = "BILL_1_RON.jpg"
    BILL_5_RON = "BILL_5_RON.jpg"
    BILL_10_RON = "BILL_10_RON.jpg"
    BILL_50_RON = "BILL_50_RON.jpg"
    
    SONG_PATH = "Music//PACANELE.ogg"

    BOX_SIZE = 130
    GAP_SIZE = 10
    BILL_WIDTH = 235
    BILL_HEIGHT = BOX_SIZE
    NR_PREV_COLORS = 7
    PREVIOUS_RESULTS_LEFT_MARGIN = (Constants.WINDOW_WIDTH - NR_PREV_COLORS * BOX_SIZE - (NR_PREV_COLORS - 1) * GAP_SIZE) // 2
    
    TEXT_FONT = "felixtitling"
    TEXT_FONT_SIZE = 256
    TEXT_FONT_COLOR = Constants.GOLD
    
    MONEY_TEXT_FONT = "lucidasans"
    MONEY_TEXT_FONT_SIZE = 20
    MONEY_TEXT_COLOR = Constants.LIGHT_ORANGE
    MONEY_TEXT_ROW_HEIGHT = 50
    
    BG_COLOR = Constants.NAVY_RED
    LIGHT_BG_COLOR = Constants.GRAY
    
    def __init__(self, gameDisplay, musicPlayer):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        
        self.__font = pygame.font.SysFont(PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.TEXT_FONT_SIZE, True, False)
        self.__aceOfSpades = self.__loadSpecialImage(PacaneleScreen.ACE_OF_SPADES_IMAGE)
        self.__aceOfHearts = self.__loadSpecialImage(PacaneleScreen.ACE_OF_HEARTS_IMAGE)
        self.__saveIcon = self.__loadSpecialImage(PacaneleScreen.SAVE_ICON_IMAGE)
        self.__1RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_1_RON)
        self.__5RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_5_RON)
        self.__10RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_10_RON)
        self.__50RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_50_RON)
        
        self.__lastColors = [-1] * PacaneleScreen.NR_PREV_COLORS
        self.__pacaneleFont = pygame.font.SysFont(PacaneleScreen.TEXT_FONT, PacaneleScreen.TEXT_FONT_SIZE, True)
        
        self.__previousSongTime = 0
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(PacaneleScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        self.__previousSongTime = Song(PacaneleScreen.SONG_PATH).play(Constants.NORMAL_VOLUME, -1, 0)
        
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
    
    def __displayLastColors(self):
        for i in range(PacaneleScreen.NR_PREV_COLORS):
            if self.__lastColors[i] == 0:
                self.__gameDisplay.blit(self.__aceOfHearts, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN+ i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), Constants.WINDOW_HEIGHT // 4))
            elif self.__lastColors[i] == 1:
                self.__gameDisplay.blit(self.__aceOfSpades, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), Constants.WINDOW_HEIGHT // 4))
            else:
                pygame.draw.rect(self.__gameDisplay, PacaneleScreen.LIGHT_BG_COLOR, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE))
    
    def __displayContent(self, moneyLeft, currentBet):        
        totalMoneyText = Text("Left: %.2f lei" % moneyLeft, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR)
        Label(Constants.WINDOW_HEIGHT / 2 - PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, Constants.WINDOW_WIDTH / 2 - len(totalMoneyText.content) * PacaneleScreen.MONEY_TEXT_FONT_SIZE / 2, -1, PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, PacaneleScreen.BG_COLOR, totalMoneyText).display(self.__gameDisplay)
        
        currentBetText = Text("Current bet: %.2f lei" % currentBet, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR)
        Label(Constants.WINDOW_HEIGHT / 2, Constants.WINDOW_WIDTH / 2 - len(currentBetText.content) * PacaneleScreen.MONEY_TEXT_FONT_SIZE / 2, -1, PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, PacaneleScreen.BG_COLOR, currentBetText).display(self.__gameDisplay)
        
        # normally these could just be blitted once when we enter the pacanele screen - however, because of the text we need to reblit
        # the background => these are covered => it's necessary that we do this
        self.__gameDisplay.blit(self.__aceOfHearts, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__aceOfSpades, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__saveIcon, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 6 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__1RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
        self.__gameDisplay.blit(self.__5RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH, 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
        self.__gameDisplay.blit(self.__10RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 2 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
        self.__gameDisplay.blit(self.__50RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
    
    def __checkResult(self, choice):
        actualResult = random.randint(0, 1)
        self.__lastColors.insert(0, actualResult)
        self.__lastColors.pop()
        
        return actualResult == choice
    
    def __resultScreen(self, result):
        if result == True:
            textBlock = self.__pacaneleFont.render("WIN", True, PacaneleScreen.TEXT_FONT_COLOR)
        else:
            textBlock = self.__pacaneleFont.render("LOSS", True, PacaneleScreen.TEXT_FONT_COLOR)
        textRect = textBlock.get_rect()
        textRect.center = (Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT / 2)
        self.__gameDisplay.blit(textBlock, textRect)
        
        pygame.display.update()
        pygame.time.wait(1000)
    
    def __redOrBlack(self, moneyLeft):
        mouseX = mouseY = 0
        choice = -1
        currentBet = 0
        
        redBox = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        blackBox = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        saveBox = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 6 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        box1Ron = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        box5Ron = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH, 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        box10Ron = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 2 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        box50Ron = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        billList = [(box1Ron, 1), (box5Ron, 5), (box10Ron, 10), (box50Ron, 50)]
        
        self.setBackgroundImage()
        self.__displayLastColors()
        self.__displayContent(moneyLeft, currentBet)
        pygame.display.update()
        
        while True:
            mouseClicked = False
            pygame.time.wait(1)
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return moneyLeft
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    mouseClicked = True
                    
            if mouseClicked == True:
                clickedBill = False
                for bill in billList: #bill[0] = the rect object; bill[1] = the value of the bill
                    if bill[0].collidepoint(mouseX, mouseY) and bill[1] <= moneyLeft:
                        currentBet += bill[1]
                        moneyLeft -= bill[1]
                        clickedBill = True
                        break
                    
                if clickedBill == False:
                    if saveBox.collidepoint(mouseX, mouseY):
                        moneyLeft += currentBet
                        return moneyLeft
                    
                    if redBox.collidepoint(mouseX, mouseY):
                        choice = 0
                    elif blackBox.collidepoint(mouseX, mouseY):
                        choice = 1
                    else:
                        continue
                    
                    if self.__checkResult(choice):
                        currentBet *= 2.0
                        self.__resultScreen(True)
                        
                    else:
                        currentBet = 0.0
                        self.__resultScreen(False)
                    
                self.setBackgroundImage()
                self.__displayLastColors()
                self.__displayContent(moneyLeft, currentBet)
                pygame.display.update()
    
    def displayContent(self, money):
        self.setBackgroundMusic()
        pygame.mouse.set_visible(True)

        functionResult = self.__redOrBlack(money)
        
        # exit from pacanele => restore the mouse cursor and the music player
        self.__musicPlayer.restorePreviousSong(self.__previousSongTime)
        pygame.mouse.set_visible(False)

        money = functionResult             
        return money
    
    
    