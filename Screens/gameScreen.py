from Screens.screen import Screen
import pygame, os
from pygame.constants import QUIT, KEYUP, K_ESCAPE, MOUSEMOTION, MOUSEBUTTONUP, K_RIGHT, KEYDOWN
from constants import Constants
from board import Board, random
from Screens.pacaneleScreen import PacaneleScreen
from soundCue import SoundCue
from text import Text
from button import Button
from moneyStorage import MoneyStorage

class GameScreen(Screen):
    INTELIGENT_SOUND_PATH = "Music//INTELIGENT_1.ogg"
    SERGHEI_SOUND_PATH = "Music//SERGHEI_RAS.ogg"
    
    BOX_SIZE = 130
    BOX_COLOR = Constants.WHITE
    GAP_SIZE = 10
    
    GAME_DIFFICULTY = 1.0 #base value
    
    BASE_BOX_REVEAL_SPEED = 360 // Constants.FPS
    BOX_REVEAL_SPEED = BASE_BOX_REVEAL_SPEED
    NR_REVEALED_BOXES = 10
    NR_OF_LEVELS = 3
    END_LEVEL_FLASH_COUNT = 10
    BASE_INCREASE_MONEY_AMOUNT = 10
    INCREASE_MONEY_AMOUNT = BASE_INCREASE_MONEY_AMOUNT
    LEFT_MARGIN = int((Constants.WINDOW_WIDTH - (Board.BOARD_WIDTH * (BOX_SIZE + GAP_SIZE) - GAP_SIZE)) / 2)
    TOP_MARGIN = int((Constants.WINDOW_HEIGHT - (Board.BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE) - GAP_SIZE)) / 2)
    BASE_IMAGE_DISPLAY_TIME = 750
    IMAGE_DISPLAY_TIME = BASE_IMAGE_DISPLAY_TIME
    
    TEXT_FONT = "lucidasans"
    TEXT_FONT_SIZE = 20
    TEXT_COLOR = Constants.LIGHT_ORANGE
    TEXT_LEFT_MARGIN = 35
    TEXT_TOP_MARGIN = 20
    TEXT_ROW_HEIGHT = 50
    
    HIGHLIGHT_COLOR = Constants.LIGHT_ORANGE
    HIGHLIGHT_BORDER_SIZE = 5
    
    DOUBLE_MONEY_BOX_WIDTH = 125
    DOUBLE_MONEY_BOX_HEIGHT = 50
    DOUBLE_MONEY_BOX_LEFT = Constants.WINDOW_WIDTH - (LEFT_MARGIN + DOUBLE_MONEY_BOX_WIDTH) // 2
    DOUBLE_MONEY_BOX_TOP = Constants.WINDOW_HEIGHT - TOP_MARGIN - DOUBLE_MONEY_BOX_HEIGHT
    
    QUIT_PROMPT_TEXT_FONT = "lucidasans"
    QUIT_PROMPT_TEXT_TOP_COORD = Constants.WINDOW_HEIGHT - 350
    QUIT_PROMPT_TEXT_LEFT_COORD = TEXT_LEFT_MARGIN
    QUIT_PROMPT_TEXT_SIZE = TEXT_FONT_SIZE
    QUIT_PROMPT_TEXT_COLOR = TEXT_COLOR
    
    BG_COLOR = Constants.NAVY_BLUE
    LIGHT_BG_COLOR = Constants.GRAY
    
    def __init__(self, gameDisplay, musicPlayer, statsRepository):
        self.__gameDisplay = gameDisplay
        self.__musicPlayer = musicPlayer
        self.__statsRepository = statsRepository
        
        self.__board = Board()
        self.__clock = pygame.time.Clock()
        self.__pacaneleScreen = PacaneleScreen(self.__gameDisplay, self.__musicPlayer, self.__statsRepository)
        
        self.__mouseX = 0
        self.__mouseY = 0
        self.__mouseClicked = False
        
        self.__totalMoves = 0
        self.__totalTime = 0
        self.__money = MoneyStorage().loadMoney()
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(GameScreen.BG_COLOR)
    
    def setBackgroundMusic(self):
        pass
    
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special_images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
    
    def __getTopLeftCoords(self, i, j):
        top = GameScreen.TOP_MARGIN + i * (GameScreen.BOX_SIZE + GameScreen.GAP_SIZE)
        left = GameScreen.LEFT_MARGIN + j * (GameScreen.BOX_SIZE + GameScreen.GAP_SIZE)
        return (top, left)
    
    def __getBoxAtCoords(self, x, y):
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                (top, left) = self.__getTopLeftCoords(i, j)
                if (left <= x <= left + GameScreen.BOX_SIZE and top <= y <= top + GameScreen.BOX_SIZE):
                    return (i, j)
                
        return (None, None)
    
    def __drawHighlightBox(self, i, j):
        (top, left) = self.__getTopLeftCoords(i, j)
        pygame.draw.rect(self.__gameDisplay, GameScreen.HIGHLIGHT_COLOR, (left - GameScreen.HIGHLIGHT_BORDER_SIZE, top - GameScreen.HIGHLIGHT_BORDER_SIZE, GameScreen.BOX_SIZE + 2 * GameScreen.HIGHLIGHT_BORDER_SIZE, GameScreen.BOX_SIZE + 2 * GameScreen.HIGHLIGHT_BORDER_SIZE), GameScreen.HIGHLIGHT_BORDER_SIZE)
    
    def __displayBoard(self):
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                (top, left) = self.__getTopLeftCoords(i, j)
                if self.__board.isRevealed(i, j):
                    currentObject = self.__gameDisplay.blit(self.__board.getImage(i, j).imageObject, (left, top))
                else:
                    currentObject = pygame.draw.rect(self.__gameDisplay, GameScreen.BOX_COLOR, (left, top, GameScreen.BOX_SIZE, GameScreen.BOX_SIZE)) 
                pygame.display.update(currentObject)
    
    def __displayBoxCoverage(self, boxList, coverage, fullyCovered = False):
        for box in boxList:
            (top, left) = self.__getTopLeftCoords(box[0], box[1])
            if fullyCovered == False:
                self.__gameDisplay.blit(self.__board.getImage(box[0], box[1]).imageObject, (left, top))
            if coverage > 0:
                pygame.draw.rect(self.__gameDisplay, GameScreen.BOX_COLOR, (left, top, coverage, GameScreen.BOX_SIZE)) 
        pygame.display.update() 
        self.__clock.tick(Constants.FPS)
    
    def __revealBoxesAnimation(self, boxList):
        for coverage in range(GameScreen.BOX_SIZE, -1, -GameScreen.BOX_REVEAL_SPEED):
            self.__displayBoxCoverage(boxList, coverage)
        self.__displayBoxCoverage(boxList, 0)
            
    def __coverBoxesAnimation(self, boxList):
        for coverage in range(0, GameScreen.BOX_SIZE + 1, GameScreen.BOX_REVEAL_SPEED):
            self.__displayBoxCoverage(boxList, coverage)
        self.__displayBoxCoverage(boxList, GameScreen.BOX_SIZE, True)
    
    def __introBoardAnimation(self):
        nrBoxes = Board.BOARD_HEIGHT * Board.BOARD_WIDTH
        auxList = list(range(nrBoxes))
        random.shuffle(auxList)
        boxList = []
        
        for index in auxList:
            i = (index // self.__board.width)
            j = (index - i * self.__board.width)
            boxList.append((i, j))
        
        self.__displayBoard()
        pygame.time.wait(100)
        
        for i in range(nrBoxes // GameScreen.NR_REVEALED_BOXES):
            self.__revealBoxesAnimation(boxList[i * GameScreen.NR_REVEALED_BOXES : (i + 1) * GameScreen.NR_REVEALED_BOXES])
            self.__coverBoxesAnimation(boxList[i * GameScreen.NR_REVEALED_BOXES : (i + 1) * GameScreen.NR_REVEALED_BOXES])
    
    def __imagesMatch(self, image1, image2):
        if image1.title == image2.title:
            return True
        
        for specialPair in self.__board.specialPairs:
            if specialPair == (image1, image2) or specialPair == (image2, image1):
                return True
            
        return False
    
    def __reshuffleHiddenTiles(self):
        # no reshuffling in easy mode
        if (GameScreen.GAME_DIFFICULTY == Constants.EASY_DIFFICULTY_MULTIPLIER):
            return
        
        if self.__totalMoves % (int)(36 / GameScreen.GAME_DIFFICULTY) == 0:
            self.__board.reshuffleHiddenTiles()
    
    def __displayCompletedAchievement(self, achievement):
        if achievement.soundCue != None:
            achievement.soundCue.play()
        
        section = pygame.Rect(GameScreen.LEFT_MARGIN, Constants.WINDOW_HEIGHT - GameScreen.TEXT_ROW_HEIGHT - GameScreen.TEXT_TOP_MARGIN, Constants.WINDOW_WIDTH - 2 * GameScreen.LEFT_MARGIN, GameScreen.TEXT_ROW_HEIGHT + GameScreen.TEXT_TOP_MARGIN)
        pygame.draw.rect(self.__gameDisplay, GameScreen.BG_COLOR, section)
        Text("Achievement unlocked: %s" % achievement.title, GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR).display(self.__gameDisplay, Constants.WINDOW_HEIGHT - GameScreen.TEXT_ROW_HEIGHT - GameScreen.TEXT_TOP_MARGIN , GameScreen.LEFT_MARGIN)
        pygame.display.update(section)
        pygame.time.delay(Constants.COMPLETED_ACHIEVEMENT_DISPLAY_TIME)
        pygame.draw.rect(self.__gameDisplay, GameScreen.BG_COLOR, section) # clear the text
    
    def __processAchievement(self, achievementCheckFunction, *arguments):
        numberOfArguments = {
            self.__statsRepository.foundImage : 1,
            self.__statsRepository.foundSoundCue : 1,
            self.__statsRepository.endLevel : 0,
            self.__statsRepository.foundCombo : 2,
        }
        
        try:
            currentNumberOfArguments = numberOfArguments[achievementCheckFunction]
            
            completedAchievements = []
            # I hope there's a shorter method of doing this, sth more general without needing an if for each no of args
            # ALso I can't just do function(arguments) in this case!
            if currentNumberOfArguments == 0: 
                completedAchievements = achievementCheckFunction()
            elif currentNumberOfArguments == 1: 
                completedAchievements = achievementCheckFunction(arguments[0])
            elif currentNumberOfArguments == 2:
                completedAchievements = achievementCheckFunction(arguments[0], arguments[1])
            
            for achievement in completedAchievements:
                self.__displayCompletedAchievement(achievement)
                
        except Exception as e:
            print ("exception: " + str(e))
    
    def __convertTime(self, ms):
        minutes = ms / 60000
        ms %= 60000
        seconds = ms / 1000
        ms = (ms % 1000) / 10
        return ("%02d:%02d:%02d" % (minutes, seconds, ms))  
    
    def __displayGameInfo(self, timePassed, nrMoves, level):
        Text(("Current moves = %d" % nrMoves), GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR).display(self.__gameDisplay, GameScreen.TEXT_TOP_MARGIN, GameScreen.TEXT_LEFT_MARGIN)
        Text(("Total moves = %d" % self.__totalMoves), GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR).display(self.__gameDisplay, GameScreen.TEXT_TOP_MARGIN + GameScreen.TEXT_ROW_HEIGHT, GameScreen.TEXT_LEFT_MARGIN)
        Text(("%.2f lei" % (self.__money / Constants.MONEY_AMOUNT_MODIFIER)), GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR).display(self.__gameDisplay, GameScreen.TEXT_TOP_MARGIN + 2 * GameScreen.TEXT_ROW_HEIGHT, GameScreen.TEXT_LEFT_MARGIN)
        Text(("Level = %d / %d" % (level, GameScreen.NR_OF_LEVELS)), GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR).display(self.__gameDisplay, GameScreen.TEXT_TOP_MARGIN + 3 * GameScreen.TEXT_ROW_HEIGHT, GameScreen.TEXT_LEFT_MARGIN)
        Text(self.__convertTime(timePassed), GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR).display(self.__gameDisplay, Constants.WINDOW_HEIGHT - 2 * GameScreen.TEXT_ROW_HEIGHT - GameScreen.TEXT_TOP_MARGIN, GameScreen.TEXT_LEFT_MARGIN)
        Text(self.__convertTime(self.__totalTime), GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR).display(self.__gameDisplay, Constants.WINDOW_HEIGHT - GameScreen.TEXT_ROW_HEIGHT - GameScreen.TEXT_TOP_MARGIN, GameScreen.TEXT_LEFT_MARGIN)
            
    def __endLevelAnimation(self):
        for i in range(GameScreen.END_LEVEL_FLASH_COUNT):
            if i % 2 == 0:
                self.__gameDisplay.fill(GameScreen.LIGHT_BG_COLOR)
            else:
                self.__gameDisplay.fill(GameScreen.BG_COLOR)
            self.__displayBoard()
            pygame.display.update()
            pygame.time.wait(300)
    
    def __displayPacaneleButton(self):
        pacaneleButtonText = Text("Dubleaza", GameScreen.TEXT_FONT, GameScreen.TEXT_FONT_SIZE, GameScreen.TEXT_COLOR)
        pacaneleButton = Button(GameScreen.DOUBLE_MONEY_BOX_TOP, GameScreen.DOUBLE_MONEY_BOX_LEFT, GameScreen.DOUBLE_MONEY_BOX_WIDTH, GameScreen.DOUBLE_MONEY_BOX_HEIGHT, GameScreen.LIGHT_BG_COLOR, pacaneleButtonText)
        pacaneleButton.display(self.__gameDisplay)
        
        if pacaneleButton.collides(self.__mouseX, self.__mouseY):
            pacaneleButton.drawHighlight(self.__gameDisplay, GameScreen.HIGHLIGHT_COLOR, GameScreen.HIGHLIGHT_BORDER_SIZE)
            if self.__mouseClicked and self.__money > 0.0:
                self.__money = self.__pacaneleScreen.displayContent(self.__money)
    
    def setGameDifficulty(self, gameDifficulty):
        GameScreen.GAME_DIFFICULTY = gameDifficulty
        GameScreen.BOX_REVEAL_SPEED = (int)(GameScreen.BASE_BOX_REVEAL_SPEED * GameScreen.GAME_DIFFICULTY)
        GameScreen.IMAGE_DISPLAY_TIME = (int)(GameScreen.BASE_IMAGE_DISPLAY_TIME // GameScreen.GAME_DIFFICULTY)
        GameScreen.INCREASE_MONEY_AMOUNT = GameScreen.BASE_INCREASE_MONEY_AMOUNT * GameScreen.GAME_DIFFICULTY
        
    def __quitGamePrompt(self):
        Text("Really want to quit ? (y/n)", GameScreen.QUIT_PROMPT_TEXT_FONT, GameScreen.QUIT_PROMPT_TEXT_SIZE, GameScreen.QUIT_PROMPT_TEXT_COLOR).display(self.__gameDisplay, GameScreen.QUIT_PROMPT_TEXT_TOP_COORD, GameScreen.QUIT_PROMPT_TEXT_LEFT_COORD)
        pygame.display.update()
        
        while True:
            pygame.time.wait(1)
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
                if event.type == KEYDOWN:
                    if event.unicode in "yY":
                        return Screen.QUIT_PROGRAM
                    if event.unicode in "nN":
                        return Screen.CONTINUE_PROGRAM
        
    def __playLevel(self, level):
        self.__board.newLevel(level)
        
        self.setBackgroundImage()
        pygame.time.wait(100)
        
        self.__introBoardAnimation()
        firstBox = None
        nrRevealed = 0
        nrMoves = 0
        timePassed = 0
        
        while True:
            pygame.time.wait(1)
            self.__mouseClicked = False
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    if self.__quitGamePrompt() == Screen.QUIT_PROGRAM:
                        return Screen.QUIT_PROGRAM
                elif event.type == MOUSEMOTION:
                    self.__mouseX, self.__mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    self.__mouseX, self.__mouseY = event.pos
                    self.__mouseClicked = True
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__musicPlayer.nextSong()
                elif event.type == SoundCue.SOUND_CUE_END_EVENT:
                    self.__musicPlayer.fadeIn() 
                    
            self.setBackgroundImage()
            self.__displayGameInfo(timePassed, nrMoves, level)
            self.__musicPlayer.displayButtons()
            if self.__mouseClicked:
                self.__musicPlayer.checkInput(self.__mouseX, self.__mouseY)
            self.__displayPacaneleButton()
            
            self.__displayBoard()
            
            (xBox, yBox) = self.__getBoxAtCoords(self.__mouseX, self.__mouseY)
            if xBox != None and yBox != None:
                if self.__board.isRevealed(xBox, yBox) == False:
                    self.__drawHighlightBox(xBox, yBox)
                    
                    if self.__mouseClicked:
                        self.__board.revealBox(xBox, yBox)
                        self.__revealBoxesAnimation([(xBox, yBox)])
                        
                        if firstBox == None:
                            firstBox = (xBox, yBox)
                        else:
                            image1 = self.__board.getImage(firstBox[0], firstBox[1])
                            image2 = self.__board.getImage(xBox, yBox)
                            
                            nrMoves += 1
                            self.__totalMoves += 1
                            
                            self.__reshuffleHiddenTiles()
                            
                            if self.__imagesMatch(image1, image2):
                                if image1.soundCue != None:
                                    SoundCue(image1.soundCue).play()
                                elif image2.soundCue != None:
                                    SoundCue(image2.soundCue).play()
                                    
                                self.__statsRepository.foundCorrectImage(1)
                                self.__statsRepository.revealedImage(1)
                                
                                nrRevealed += 2
                                self.__money += GameScreen.INCREASE_MONEY_AMOUNT
                                self.__statsRepository.earnedMoney(GameScreen.INCREASE_MONEY_AMOUNT / Constants.MONEY_AMOUNT_MODIFIER)
                                self.__processAchievement(self.__statsRepository.foundImage, image1.title)
                                self.__processAchievement(self.__statsRepository.foundImage, image2.title)
                                # we put both pictures in here because we might have a special pair
                                # otherwise, "finding" the same image twice will not affect the achievement
                                
                                self.__processAchievement(self.__statsRepository.foundCombo, image1.title, self.__musicPlayer.getCurrentSong().title)
                                self.__processAchievement(self.__statsRepository.foundCombo, image2.title, self.__musicPlayer.getCurrentSong().title)
                                
                                # we check this before the level-ending condition so that we don't lose any sound cues that might appear right at the end
                                # (they won't be played, but will be taken into consideration for the achievements)
                                if image1.soundCue != None:
                                    self.__processAchievement(self.__statsRepository.foundSoundCue, image1.soundCue)
                                
                                if nrRevealed == self.__board.height * self.__board.width:  
                                #if nrRevealed == 2: 
                                    if nrMoves == self.__board.height * self.__board.width // 2: # perfect level achievement
                                        self.__processAchievement(self.__statsRepository.endLevel)
                                    return
                            
                            else:
                                self.__statsRepository.foundWrongImage(1)
                                self.__statsRepository.revealedImage(1)
                                
                                pygame.time.wait(GameScreen.IMAGE_DISPLAY_TIME)
                                self.__coverBoxesAnimation([(firstBox[0], firstBox[1]), (xBox, yBox)])
                                self.__board.coverBox(firstBox[0], firstBox[1])
                                self.__board.coverBox(xBox, yBox)
                                
                            firstBox = None
                            
            pygame.display.update()
            self.__clock.tick(Constants.FPS)
            
            timePassed += self.__clock.get_time()
            self.__totalTime += self.__clock.get_time()
    
    def displayContent(self):
        self.__statsRepository.startGame(1)
        currentVolume = Constants.NORMAL_VOLUME
        
        for level in range(1, GameScreen.NR_OF_LEVELS + 1):        # level indexing starts at 1
            currentVolume = pygame.mixer.music.get_volume()
            levelResult = self.__playLevel(level)
            if levelResult == Screen.QUIT_PROGRAM:
                pygame.mouse.set_visible(True)
                MoneyStorage().saveMoney(self.__money)
                self.__statsRepository.exitLevel(self.__totalTime) # the level can be exited either when finishing it or when pressing the ESC key
                return (Screen.QUIT_PROGRAM, Screen.QUIT_PROGRAM)
            
            if level == GameScreen.NR_OF_LEVELS:
                SoundCue(GameScreen.INTELIGENT_SOUND_PATH).play()
            else:
                SoundCue(GameScreen.SERGHEI_SOUND_PATH).play()
            
            self.__endLevelAnimation()
            pygame.time.wait(2200) #PSA: don't have task manager open when ending a level, apparently wait() behaves weirdly
            
        pygame.mixer.music.set_volume(currentVolume) #restore the music volume after exiting the last level

        MoneyStorage().saveMoney(self.__money)
        self.__statsRepository.exitLevel(self.__totalTime)
        self.__statsRepository.finishGame(1)
        return (self.__totalTime, self.__totalMoves)
