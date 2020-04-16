import pygame
from pygame.constants import *
from constants import *
from board import Board
import random
from audioRepo import AudioRepo
from leaderboard import Leaderboard
from doubleMoney import DoubleMoney

class GUI:
    def __init__(self):
        self.__board = Board()
        self.__imageRepo = self.__board.imageRepo
        self.__audioRepo = AudioRepo()
        self.__fastLeader = Leaderboard("fast.pickle")
        self.__smartLeader = Leaderboard("smart.pickle")
        
        pygame.init()
        pygame.display.set_caption(APP_TITLE)
        pygame.display.set_icon(self.__imageRepo.SERGHEI_ICON1)
        
        self.__gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.SysFont(TEXT_FONT, TEXT_FONT_SIZE, True, False)
        
        self.__doubleMoney = DoubleMoney(self.__gameDisplay, self.__font, self.__audioRepo, self.__imageRepo.ACE_HEARTS, self.__imageRepo.ACE_SPADES, self.__imageRepo.SAVE_ICON)
        
        self.__mouseX = 0
        self.__mouseY = 0
        self.__mouseClicked = False
        
        self.__totalMoves = 0
        self.__totalTime = 0
        self.__money = 0.0
        
        pygame.mouse.set_visible(False)
        
    def __quitGame(self):
        self.__gameDisplay.blit(self.__imageRepo.EXIT_SCREEN_1, (0, 0))
        pygame.display.update()
        pygame.time.wait(2000)
        self.__gameDisplay.blit(self.__imageRepo.EXIT_SCREEN_2, (0, 0))
        pygame.display.update()
        pygame.time.wait(2000)
        self.__audioRepo.fadeOut()
        pygame.quit()
        quit()    
        
    def __introScreenTransition(self):
        leftMargin = 0
        while leftMargin <= WINDOW_WIDTH:
            self.__gameDisplay.fill(BG_COLOR)
            self.__gameDisplay.blit(self.__imageRepo.WELCOME_SCREEN, (leftMargin, 0))
            pygame.display.update()
            pygame.time.wait(TRANSITION_TIME // TRANSITION_STEPS)
            leftMargin += WINDOW_WIDTH // TRANSITION_STEPS
        
    def __welcomeScreen(self):
        running = True
        self.__audioRepo.playIntroSong()
        while running:
            self.__gameDisplay.blit(self.__imageRepo.WELCOME_SCREEN, (0, 0))
            for event in pygame.event.get(): 
                if event.type == KEYUP and event.key == K_RETURN:
                    running = False
                    self.__introScreenTransition()
                elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.__quitGame()
            pygame.display.update()
    
    def __getTopLeftCoords(self, i, j):
        top = TOP_MARGIN + i * (BOX_SIZE + GAP_SIZE)
        left = LEFT_MARGIN + j * (BOX_SIZE + GAP_SIZE)
        return (top, left)
    
    def __getBoxAtCoords(self, x, y):
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                (top, left) = self.__getTopLeftCoords(i, j)
                if (left <= x <= left + BOX_SIZE and top <= y <= top + BOX_SIZE):
                    return (i, j)
                
        return (None, None)
    
    def __drawHighlightBox(self, i, j):
        (top, left) = self.__getTopLeftCoords(i, j)
        pygame.draw.rect(self.__gameDisplay, HIGHLIGHT_COLOR, (left - HIGHLIGHT_BORDER_SIZE, top - HIGHLIGHT_BORDER_SIZE, BOX_SIZE + 2 * HIGHLIGHT_BORDER_SIZE, BOX_SIZE + 2 * HIGHLIGHT_BORDER_SIZE), HIGHLIGHT_BORDER_SIZE)
    
    def __displayBoard(self):
        for i in range(self.__board.height):
            for j in range(self.__board.width):
                (top, left) = self.__getTopLeftCoords(i, j)
                if self.__board.isRevealed(i, j):
                    self.__gameDisplay.blit(self.__board.getImage(i, j), (left, top))
                else:
                    pygame.draw.rect(self.__gameDisplay, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE)) 
        pygame.display.update()
    
    def __displayBoxCoverage(self, boxList, coverage):
        for box in boxList:
            (top, left) = self.__getTopLeftCoords(box[0], box[1])
            self.__gameDisplay.blit(self.__board.getImage(box[0], box[1]), (left, top))
            if coverage > 0:
                pygame.draw.rect(self.__gameDisplay, BOX_COLOR, (left, top, coverage, BOX_SIZE)) 
        pygame.display.update() 
        self.__clock.tick(FPS)
    
    def __revealBoxesAnimation(self, boxList):
        for coverage in range(BOX_SIZE, -1, -BOX_REVEAL_SPEED):
            self.__displayBoxCoverage(boxList, coverage)
        self.__displayBoxCoverage(boxList, 0)
            
    def __coverBoxesAnimation(self, boxList):
        for coverage in range(0, BOX_SIZE + 1, BOX_REVEAL_SPEED):
            self.__displayBoxCoverage(boxList, coverage)
        self.__displayBoxCoverage(boxList, BOX_SIZE)
        
    def __displayText(self, text, xPos, yPos, font, color):
        self.__gameDisplay.blit(font.render(text, True, color, None), (xPos, yPos))   
        
    def __convertTime(self, ms):
        minutes = ms / 60000
        ms %= 60000
        seconds = ms / 1000
        ms %= 1000
        return ("%02d:%02d:%03d" % (minutes, seconds, ms))    
        
    def __displayInfo(self, timePassed, nrMoves, level):
        self.__displayText(("Current moves = %d" % nrMoves), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN, self.__font, TEXT_COLOR)
        self.__displayText(("Total moves = %d" % self.__totalMoves), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN + TEXT_ROW_HEIGHT, self.__font, TEXT_COLOR) 
        self.__displayText(("%.2f lei" % self.__money), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN + 2 * TEXT_ROW_HEIGHT, self.__font, TEXT_COLOR)
        self.__displayText(("Level = %d / %d" % (level, NR_OF_LEVELS)), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN + 3 * TEXT_ROW_HEIGHT, self.__font, TEXT_COLOR)
        self.__displayText(self.__convertTime(timePassed), TEXT_LEFT_MARGIN, WINDOW_HEIGHT - 2 * TEXT_ROW_HEIGHT - TEXT_TOP_MARGIN, self.__font, TEXT_COLOR)
        self.__displayText(self.__convertTime(self.__totalTime), TEXT_LEFT_MARGIN, WINDOW_HEIGHT - TEXT_ROW_HEIGHT - TEXT_TOP_MARGIN, self.__font, TEXT_COLOR)
    
    def __introBoardAnimation(self):
        nrBoxes = BOARD_HEIGHT * BOARD_WIDTH
        auxList = list(range(nrBoxes))
        random.shuffle(auxList)
        boxList = []
        
        for index in auxList:
            i = (index // self.__board.width)
            j = (index - i * self.__board.width)
            boxList.append((i, j))
        
        self.__displayBoard()
        pygame.time.wait(100)
        
        for i in range(nrBoxes // NR_REVEALED_BOXES):
            self.__revealBoxesAnimation(boxList[i * NR_REVEALED_BOXES : (i + 1) * NR_REVEALED_BOXES])
            self.__coverBoxesAnimation(boxList[i * NR_REVEALED_BOXES : (i + 1) * NR_REVEALED_BOXES])
            
    def __endLevelAnimation(self):
        for i in range(END_LEVEL_FLASHES):
            if i % 2 == 0:
                self.__gameDisplay.fill(LIGHT_BG_COLOR)
            else:
                self.__gameDisplay.fill(BG_COLOR)
            self.__displayBoard()
            pygame.display.update()
            pygame.time.wait(300)
    
    def __mouseCursor(self):
        self.__gameDisplay.blit(self.__imageRepo.MOUSE_CURSOR, (self.__mouseX, self.__mouseY))
    
    def __userInput(self):
        userInput = ""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.__quitGame()
                if event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__audioRepo.nextSong()
                if event.type == KEYDOWN:
                    if len(userInput) < MAX_NAME_LENGTH and (event.unicode.isalnum() or event.unicode in "!@#$%^&*()_+-=<>,.?/:{}\|`~ '"):
                        userInput += event.unicode
                    elif event.key == K_BACKSPACE:
                        userInput = userInput[:-1]
                    elif event.key == K_RETURN:
                        return userInput
                    
            self.__gameDisplay.fill(BG_COLOR)
            self.__displayText("baga un nume", WINDOW_WIDTH / 2 - 12 * 7, WINDOW_HEIGHT / 2 - 2 * TEXT_ROW_HEIGHT, self.__font, LIGHT_ORANGE)
            
            pygame.draw.rect(self.__gameDisplay, LIGHT_BG_COLOR, (WINDOW_WIDTH / 2 - 250, WINDOW_HEIGHT / 2 - TEXT_ROW_HEIGHT / 2, 500, TEXT_ROW_HEIGHT))
            
            textBlock = self.__font.render(userInput, True, LIGHT_ORANGE)
            textRect = textBlock.get_rect()
            textRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            self.__gameDisplay.blit(textBlock, textRect)
            
            pygame.display.update()
    
    def __displayResults(self):
        self.__displayText("rapidu", WINDOW_WIDTH / 4 - 6 * 7, WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        self.__displayText("desteptu", 3 * WINDOW_WIDTH / 4 - 6 * 7, WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        
        for i in range(TABLE_ENTRIES):
            self.__displayText("%02d. %s" % (i + 1, self.__fastLeader.scoreList[i][0]), 2 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            self.__displayText(self.__convertTime(self.__fastLeader.scoreList[i][1]), WINDOW_WIDTH / 2 - 6 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            
            self.__displayText("%02d. %s" % (i + 1, self.__smartLeader.scoreList[i][0]), WINDOW_WIDTH / 2 + 2 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
            self.__displayText("%d moves" % (self.__smartLeader.scoreList[i][1]), WINDOW_WIDTH - 6 * TEXT_LEFT_MARGIN, (i + 2) * TEXT_ROW_HEIGHT + WINDOW_HEIGHT / 4, self.__font, LIGHT_ORANGE)
        
        pygame.display.update()
    
    def __endGame(self):
        self.__gameDisplay.fill(BG_COLOR)
        self.__displayResults()
        
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.__quitGame()
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__audioRepo.nextSong()
        
    def __playLevel(self, level):
        self.__board.newLevel(level)
        #new level screen ? (sth like "level 1") - for now we'll use just a background
        
        self.__gameDisplay.fill(BG_COLOR)
        pygame.display.update()
        pygame.time.wait(100)
        
        self.__introBoardAnimation()
        firstBox = None
        nrRevealed = 0
        nrMoves = 0
        timePassed = 0
        
        while True:
            self.__mouseClicked = False
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.__quitGame()
                elif event.type == MOUSEMOTION:
                    self.__mouseX, self.__mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    self.__mouseX, self.__mouseY = event.pos
                    self.__mouseClicked = True
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__audioRepo.nextSong()
                elif event.type == self.__audioRepo.soundCueEndEvent:
                    self.__audioRepo.fadeIn() 
                    
            self.__gameDisplay.fill(BG_COLOR)
            self.__displayInfo(timePassed, nrMoves, level)
            self.__money = self.__doubleMoney.double(self.__mouseX, self.__mouseY, self.__mouseClicked, self.__money)
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
                            
                            if image1 != image2:
                                pygame.time.wait(1000)
                                self.__coverBoxesAnimation([(firstBox[0], firstBox[1]), (xBox, yBox)])
                                self.__board.coverBox(firstBox[0], firstBox[1])
                                self.__board.coverBox(xBox, yBox)
                                
                            else:
                                nrRevealed += 2
                                self.__money += INCREASE_MONEY_AMOUNT
                                
                                if nrRevealed == self.__board.height * self.__board.width:  
                                    return

                                if image1 in self.__imageRepo.imageSoundCues.keys():
                                    self.__audioRepo.playSoundCue(self.__imageRepo.imageSoundCues[image1], 3.0)
                                
                            firstBox = None
                            
            self.__mouseCursor()
            pygame.display.update()
            self.__clock.tick(FPS)
            
            timePassed += self.__clock.get_time()
            self.__totalTime += self.__clock.get_time()
        
    def __playGame(self):
        self.__audioRepo.nextSong()
        playerName = self.__userInput()
        for level in range(1, NR_OF_LEVELS + 1):        # level indexing starts at 1
            self.__playLevel(level)
            
            if level == NR_OF_LEVELS:
                self.__audioRepo.playSoundCue(INTELIGENT_SOUND_PATH, 3.0) 
            else:
                self.__audioRepo.playSoundCue(SERGHEI_SOUND_PATH, 1.0)
            
            self.__endLevelAnimation()
            pygame.time.wait(2500)
            
        newFast = self.__fastLeader.checkResult(self.__totalTime)
        if newFast == True:
            self.__fastLeader.addResult(self.__totalTime, playerName)
        newSmart = self.__smartLeader.checkResult(self.__totalMoves)
        if newSmart == True:
            self.__smartLeader.addResult(self.__totalMoves, playerName)
        
    def start(self):
        self.__welcomeScreen()
        self.__playGame()
        self.__endGame()
        
        