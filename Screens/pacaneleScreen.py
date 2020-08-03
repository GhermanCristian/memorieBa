from Screens.screen import Screen
import pygame, os, random
from constants import Constants
from song import Song
from text import Text
from label import Label
from pygame.constants import QUIT, MOUSEMOTION, K_ESCAPE, KEYUP, MOUSEBUTTONUP
from soundCue import SoundCue

class PacaneleScreen(Screen):
    ACE_OF_SPADES_IMAGE = "ACE_SPADES.jpg"
    ACE_OF_HEARTS_IMAGE = "ACE_HEARTS.jpg"
    SAVE_ICON_IMAGE = "SAVE_ICON.jpg"
    BILL_1_RON_IMAGE = "BILL_1_RON.jpg"
    BILL_5_RON_IMAGE = "BILL_5_RON.jpg"
    BILL_10_RON_IMAGE = "BILL_10_RON.jpg"
    BILL_50_RON_IMAGE = "BILL_50_RON.jpg"
    FREEDOM_IMAGE = "FREEDOM.jpg"
    TIMISOREANA_IMAGE = "TIMISOREANA.jpg"
    
    SONG_PATH = "Music//PACANELE.ogg"

    BOX_SIZE = 130
    GAP_SIZE = 10
    
    DRINK_IMAGE_LEFT_MARGIN = 50
    DRINK_IMAGE_TOP_MARGIN = 50
    DRINK_IMAGE_SIZE = BOX_SIZE
    FREEDOM_PRICE = 2.0
    TIMISOREANA_PRICE = 2.5
    
    NR_PREV_COLORS = 7
    PREVIOUS_RESULTS_LEFT_MARGIN = (Constants.WINDOW_WIDTH - NR_PREV_COLORS * BOX_SIZE - (NR_PREV_COLORS - 1) * GAP_SIZE) // 2
    PREVIOUS_RESULTS_TOP_MARGIN = Constants.WINDOW_HEIGHT // 4
    
    BILL_WIDTH = 235
    BILL_HEIGHT = BOX_SIZE
    BILL_LEFT_MARGIN = PREVIOUS_RESULTS_LEFT_MARGIN
    BILL_TOP_MARGIN = 3 * Constants.WINDOW_HEIGHT // 4 - GAP_SIZE - BILL_HEIGHT
    
    BUTTON_LEFT_MARGIN = PREVIOUS_RESULTS_LEFT_MARGIN
    BUTTON_TOP_MARGIN = 3 * Constants.WINDOW_HEIGHT // 4
    
    TEXT_FONT = "felixtitling"
    TEXT_FONT_SIZE = 256
    TEXT_FONT_COLOR = Constants.GOLD
    
    MONEY_TEXT_FONT = "lucidasans"
    MONEY_TEXT_FONT_SIZE = 20
    MONEY_TEXT_COLOR = Constants.LIGHT_ORANGE
    MONEY_TEXT_ROW_HEIGHT = 50
    MONEY_TEXT_TOP_MARGIN = 20
    
    BG_COLOR = Constants.NAVY_RED
    LIGHT_BG_COLOR = Constants.GRAY
    
    RESULT_DISPLAY_TIME = 1000
    
    PIERDUT_PACANELE_SOUND_CUE = "PIERDUT_PACANELE.ogg"
    
    def __init__(self, gameDisplay, musicPlayer, statsRepository):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        self.__statsRepository = statsRepository
        
        self.__font = pygame.font.SysFont(PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.TEXT_FONT_SIZE, True, False)
        self.__aceOfSpades = self.__loadSpecialImage(PacaneleScreen.ACE_OF_SPADES_IMAGE)
        self.__aceOfHearts = self.__loadSpecialImage(PacaneleScreen.ACE_OF_HEARTS_IMAGE)
        self.__saveIcon = self.__loadSpecialImage(PacaneleScreen.SAVE_ICON_IMAGE)
        self.__1RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_1_RON_IMAGE)
        self.__5RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_5_RON_IMAGE)
        self.__10RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_10_RON_IMAGE)
        self.__50RonBill = self.__loadSpecialImage(PacaneleScreen.BILL_50_RON_IMAGE)
        self.__freedom = self.__loadSpecialImage(PacaneleScreen.FREEDOM_IMAGE)
        self.__timisoreana = self.__loadSpecialImage(PacaneleScreen.TIMISOREANA_IMAGE)
        
        self.__lastColors = [-1] * PacaneleScreen.NR_PREV_COLORS
        self.__pacaneleFont = pygame.font.SysFont(PacaneleScreen.TEXT_FONT, PacaneleScreen.TEXT_FONT_SIZE, True)
        
        self.__previousSongTime = 0
        
        self.__pierdutPacaneleSoundCue = os.path.join(os.getcwd(), "Music")
        self.__pierdutPacaneleSoundCue = os.path.join(self.__pierdutPacaneleSoundCue, PacaneleScreen.PIERDUT_PACANELE_SOUND_CUE)
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(PacaneleScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        self.__previousSongTime = Song(PacaneleScreen.SONG_PATH).play(self.__musicPlayer.musicVolume, -1, 0)
        
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special_images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
    
    def __displayLastColors(self):
        for i in range(PacaneleScreen.NR_PREV_COLORS):
            if self.__lastColors[i] == 0:
                self.__gameDisplay.blit(self.__aceOfHearts, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), PacaneleScreen.PREVIOUS_RESULTS_TOP_MARGIN))
            elif self.__lastColors[i] == 1:
                self.__gameDisplay.blit(self.__aceOfSpades, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), PacaneleScreen.PREVIOUS_RESULTS_TOP_MARGIN))
            else:
                pygame.draw.rect(self.__gameDisplay, PacaneleScreen.LIGHT_BG_COLOR, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + i * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), PacaneleScreen.PREVIOUS_RESULTS_TOP_MARGIN, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE))
    
    def __displayText(self, moneyLeft, currentBet):        
        totalMoneyText = Text("Left: %.2f lei" % moneyLeft, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR)
        # we don't just display the text, we use labels because they will center the text
        Label(Constants.WINDOW_HEIGHT / 2 - PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, Constants.WINDOW_WIDTH / 2 - len(totalMoneyText.content) * PacaneleScreen.MONEY_TEXT_FONT_SIZE / 2, -1, PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, PacaneleScreen.BG_COLOR, totalMoneyText).display(self.__gameDisplay)
        currentBetText = Text("Current bet: %.2f lei" % currentBet, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR)
        Label(Constants.WINDOW_HEIGHT / 2, Constants.WINDOW_WIDTH / 2 - len(currentBetText.content) * PacaneleScreen.MONEY_TEXT_FONT_SIZE / 2, -1, PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, PacaneleScreen.BG_COLOR, currentBetText).display(self.__gameDisplay)
        
        Text("Freedom", PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR).display(self.__gameDisplay, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN + PacaneleScreen.DRINK_IMAGE_SIZE + PacaneleScreen.GAP_SIZE, PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN + PacaneleScreen.DRINK_IMAGE_SIZE // 2 - 50)
        Text("%.0f lei" % PacaneleScreen.FREEDOM_PRICE, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR).display(self.__gameDisplay, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN + PacaneleScreen.DRINK_IMAGE_SIZE + PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN + PacaneleScreen.DRINK_IMAGE_SIZE // 2 - 50)
        Text("Timisoreana", PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR).display(self.__gameDisplay, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN + PacaneleScreen.DRINK_IMAGE_SIZE + PacaneleScreen.GAP_SIZE, Constants.WINDOW_WIDTH - PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN - PacaneleScreen.DRINK_IMAGE_SIZE)
        Text("%.1f lei" % PacaneleScreen.TIMISOREANA_PRICE, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR).display(self.__gameDisplay, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN + PacaneleScreen.DRINK_IMAGE_SIZE + PacaneleScreen.MONEY_TEXT_ROW_HEIGHT, Constants.WINDOW_WIDTH - PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN - PacaneleScreen.DRINK_IMAGE_SIZE)

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
        textRect.center = (Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT / 2 - 50)
        # we subtract 50 pixels from the height so that the text doesn't exceed the limits of the rectangle that updates when stuff changes
        self.__gameDisplay.blit(textBlock, textRect)
        
        pygame.display.update()
        pygame.time.wait(PacaneleScreen.RESULT_DISPLAY_TIME)
    
    def __updateResultTextSection(self, moneyLeft, currentBet):
        section = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, PacaneleScreen.PREVIOUS_RESULTS_TOP_MARGIN, Constants.WINDOW_WIDTH - 2 * PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, PacaneleScreen.BILL_TOP_MARGIN - PacaneleScreen.PREVIOUS_RESULTS_TOP_MARGIN)
        pygame.draw.rect(self.__gameDisplay, PacaneleScreen.BG_COLOR, section) # reset the background image on this section
        self.__displayLastColors()
        self.__displayText(moneyLeft, currentBet)
        pygame.display.update(section)
    
    def __displayCompletedAchievement(self, achievement):
        if achievement.soundCue != None:
            achievement.soundCue.play()
        
        section = pygame.Rect(PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, Constants.WINDOW_HEIGHT - PacaneleScreen.MONEY_TEXT_ROW_HEIGHT - PacaneleScreen.MONEY_TEXT_TOP_MARGIN, Constants.WINDOW_WIDTH - 2 * PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, PacaneleScreen.MONEY_TEXT_ROW_HEIGHT + PacaneleScreen.MONEY_TEXT_TOP_MARGIN)
        pygame.draw.rect(self.__gameDisplay, PacaneleScreen.BG_COLOR, section)
        Text("Achievement unlocked: %s" % achievement.title, PacaneleScreen.MONEY_TEXT_FONT, PacaneleScreen.MONEY_TEXT_FONT_SIZE, PacaneleScreen.MONEY_TEXT_COLOR).display(self.__gameDisplay, Constants.WINDOW_HEIGHT - PacaneleScreen.MONEY_TEXT_ROW_HEIGHT - PacaneleScreen.MONEY_TEXT_TOP_MARGIN , PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN)
        pygame.display.update(section)
        pygame.time.delay(Constants.COMPLETED_ACHIEVEMENT_DISPLAY_TIME)
        pygame.draw.rect(self.__gameDisplay, PacaneleScreen.BG_COLOR, section) # clear the text
        pygame.display.update(section)
    
    def __processAchievement(self, achievementCheckFunction, *arguments):
        numberOfArguments = {
            self.__statsRepository.boughtDrink : 1,
            self.__statsRepository.madeBet : 1
        }
        
        try:
            currentNumberOfArguments = numberOfArguments[achievementCheckFunction]
            
            completedAchievements = []
            # I hope there's a shorter method of doing this, sth more general without needing an if for each no of args
            if currentNumberOfArguments == 1: 
                completedAchievements = achievementCheckFunction(arguments[0])

            for achievement in completedAchievements:
                self.__displayCompletedAchievement(achievement)
                
        except Exception:
            pass
    
    def __redOrBlack(self, moneyLeft):
        mouseX = mouseY = 0
        choice = -1
        currentBet = 0
        
        redBox = pygame.Rect(PacaneleScreen.BUTTON_LEFT_MARGIN, PacaneleScreen.BUTTON_TOP_MARGIN, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        blackBox = pygame.Rect(PacaneleScreen.BUTTON_LEFT_MARGIN + 3 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), PacaneleScreen.BUTTON_TOP_MARGIN, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        saveBox = pygame.Rect(PacaneleScreen.BUTTON_LEFT_MARGIN + 6 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), PacaneleScreen.BUTTON_TOP_MARGIN, PacaneleScreen.BOX_SIZE, PacaneleScreen.BOX_SIZE)
        
        box1Ron = pygame.Rect(PacaneleScreen.BILL_LEFT_MARGIN, PacaneleScreen.BILL_TOP_MARGIN, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        box5Ron = pygame.Rect(PacaneleScreen.BILL_LEFT_MARGIN + PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_TOP_MARGIN, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        box10Ron = pygame.Rect(PacaneleScreen.BILL_LEFT_MARGIN + 2 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), PacaneleScreen.BILL_TOP_MARGIN, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        box50Ron = pygame.Rect(PacaneleScreen.BILL_LEFT_MARGIN + 3 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), PacaneleScreen.BILL_TOP_MARGIN, PacaneleScreen.BILL_WIDTH, PacaneleScreen.BILL_HEIGHT)
        billList = [(box1Ron, 1), (box5Ron, 5), (box10Ron, 10), (box50Ron, 50)]
        
        freedomBox = pygame.Rect(PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN, PacaneleScreen.DRINK_IMAGE_SIZE, PacaneleScreen.DRINK_IMAGE_SIZE)
        timisoreanaBox = pygame.Rect(Constants.WINDOW_WIDTH - PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN - PacaneleScreen.DRINK_IMAGE_SIZE, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN, PacaneleScreen.DRINK_IMAGE_SIZE, PacaneleScreen.DRINK_IMAGE_SIZE)
        drinkList = [(freedomBox, PacaneleScreen.FREEDOM_PRICE, "freedom"), (timisoreanaBox, PacaneleScreen.TIMISOREANA_PRICE, "timisoreana")]
        
        while True:
            mouseClicked = False
            pygame.time.wait(1)
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    moneyLeft += currentBet
                    return moneyLeft
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    mouseClicked = True
                    
            if mouseClicked == True:
                alreadyClicked = False
                for bill in billList: #bill[0] = the rect object; bill[1] = the value of the bill
                    if bill[0].collidepoint(mouseX, mouseY) and bill[1] <= moneyLeft:
                        currentBet += bill[1]
                        moneyLeft -= bill[1]
                        self.__statsRepository.spentMoney(bill[1])
                        alreadyClicked = True
                        break
                    
                for drink in drinkList: #drink[0] = the rect object; drink[1] = the price of the drink; drink[2] = drink type
                    if drink[0].collidepoint(mouseX, mouseY) and drink[1] <= moneyLeft:
                        moneyLeft -= drink[1]
                        alreadyClicked = True
                        self.__processAchievement(self.__statsRepository.boughtDrink, drink[2])
                        self.__statsRepository.boughtDrinkStat(1)
                        self.__statsRepository.spentMoney(drink[1])
                        break
                
                if alreadyClicked == False:
                    if saveBox.collidepoint(mouseX, mouseY):
                        moneyLeft += currentBet
                        self.__statsRepository.earnedMoney(currentBet)
                        return moneyLeft
                    
                    # no use in clicking the red/ black buttons if there is nothing to bet
                    if currentBet == 0:
                        continue
                    
                    if redBox.collidepoint(mouseX, mouseY):
                        choice = 0
                    elif blackBox.collidepoint(mouseX, mouseY):
                        choice = 1
                    else:
                        continue
                    
                    if self.__checkResult(choice): # correct guess
                        currentBet *= 2.0
                        self.__processAchievement(self.__statsRepository.madeBet, currentBet)
                        self.__resultScreen(True)
                        
                    else:
                        self.__processAchievement(self.__statsRepository.madeBet, -currentBet)
                        currentBet = 0.0
                        if moneyLeft < 0.1: # normally it would be == 0.0 but python math is stupid
                            SoundCue(self.__pierdutPacaneleSoundCue).play()
                        self.__resultScreen(False)
                    
                self.__updateResultTextSection(moneyLeft, currentBet)
    
    def displayContent(self, money):
        self.setBackgroundMusic()
        
        self.setBackgroundImage()
        self.__updateResultTextSection(money, 0) # we can use 0 here because the initial bet is always 0
        self.__gameDisplay.blit(self.__aceOfHearts, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__aceOfSpades, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__saveIcon, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 6 * (PacaneleScreen.BOX_SIZE + PacaneleScreen.GAP_SIZE), 3 * Constants.WINDOW_HEIGHT // 4))
        self.__gameDisplay.blit(self.__1RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN, 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
        self.__gameDisplay.blit(self.__5RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH, 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
        self.__gameDisplay.blit(self.__10RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 2 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
        self.__gameDisplay.blit(self.__50RonBill, (PacaneleScreen.PREVIOUS_RESULTS_LEFT_MARGIN + 3 * (PacaneleScreen.GAP_SIZE + PacaneleScreen.BILL_WIDTH), 3 * Constants.WINDOW_HEIGHT // 4 - PacaneleScreen.GAP_SIZE - PacaneleScreen.BILL_HEIGHT))
        self.__gameDisplay.blit(self.__freedom, (PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN))
        self.__gameDisplay.blit(self.__timisoreana, (Constants.WINDOW_WIDTH - PacaneleScreen.DRINK_IMAGE_LEFT_MARGIN - PacaneleScreen.DRINK_IMAGE_SIZE, PacaneleScreen.DRINK_IMAGE_TOP_MARGIN))
        pygame.display.update()

        functionResult = self.__redOrBlack(money)
        
        # exit from pacanele => restore the music player
        self.__musicPlayer.restorePreviousSong(self.__previousSongTime)

        money = functionResult             
        return money
    
    
    