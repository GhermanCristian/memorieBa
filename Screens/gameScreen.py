from Screens.screen import Screen, QUIT_PROGRAM, CONTINUE_PROGRAM
import pygame
from pygame.constants import QUIT, KEYUP, K_ESCAPE, MOUSEMOTION, MOUSEBUTTONUP, K_RIGHT
from constants import NR_OF_LEVELS, INTELIGENT_SOUND_PATH, SERGHEI_SOUND_PATH, BG_COLOR, INCREASE_MONEY_AMOUNT, FPS, BOARD_HEIGHT,\
    BOARD_WIDTH, NR_REVEALED_BOXES, BOX_SIZE, BOX_REVEAL_SPEED, BOX_COLOR, HIGHLIGHT_BORDER_SIZE, HIGHLIGHT_COLOR, TOP_MARGIN,\
    GAP_SIZE, LEFT_MARGIN, TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN, WINDOW_HEIGHT, WINDOW_WIDTH, TEXT_COLOR, TEXT_ROW_HEIGHT,\
    TEXT_FONT, TEXT_FONT_SIZE, END_LEVEL_FLASHES, LIGHT_BG_COLOR
from board import Board, random
from Screens.pacaneleScreen import PacaneleScreen
from soundCue import SoundCue

class GameScreen(Screen):
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        
        self.__board = Board()
        self.__imageRepo = self.__board.imageRepo
        
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.SysFont(TEXT_FONT, TEXT_FONT_SIZE, True, False)
        
        self.__pacaneleScreen = PacaneleScreen(self.__gameDisplay, self.__playlist)
        
        self.__mouseX = 0
        self.__mouseY = 0
        self.__mouseClicked = False
        
        self.__totalMoves = 0
        self.__totalTime = 0
        self.__money = 0.0
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(BG_COLOR)
    
    def setBackgroundMusic(self):
        pass
    
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
    
    def __showMouseCursor(self):
        self.__gameDisplay.blit(self.__imageRepo.MOUSE_CURSOR, (self.__mouseX, self.__mouseY))
    
    def __convertTime(self, ms):
        minutes = ms / 60000
        ms %= 60000
        seconds = ms / 1000
        ms %= 1000
        return ("%02d:%02d:%03d" % (minutes, seconds, ms)) 
    
    def __displayText(self, text, xPos, yPos, font, color):
        self.__gameDisplay.blit(font.render(text, True, color, None), (xPos, yPos))      
        
    def __displayInfo(self, timePassed, nrMoves, level):
        self.__displayText(("Current moves = %d" % nrMoves), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN, self.__font, TEXT_COLOR)
        self.__displayText(("Total moves = %d" % self.__totalMoves), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN + TEXT_ROW_HEIGHT, self.__font, TEXT_COLOR) 
        self.__displayText(("%.2f lei" % self.__money), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN + 2 * TEXT_ROW_HEIGHT, self.__font, TEXT_COLOR)
        self.__displayText(("Level = %d / %d" % (level, NR_OF_LEVELS)), TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN + 3 * TEXT_ROW_HEIGHT, self.__font, TEXT_COLOR)
        self.__displayText(self.__convertTime(timePassed), TEXT_LEFT_MARGIN, WINDOW_HEIGHT - 2 * TEXT_ROW_HEIGHT - TEXT_TOP_MARGIN, self.__font, TEXT_COLOR)
        self.__displayText(self.__convertTime(self.__totalTime), TEXT_LEFT_MARGIN, WINDOW_HEIGHT - TEXT_ROW_HEIGHT - TEXT_TOP_MARGIN, self.__font, TEXT_COLOR)
    
    def __endLevelAnimation(self):
        for i in range(END_LEVEL_FLASHES):
            if i % 2 == 0:
                self.__gameDisplay.fill(LIGHT_BG_COLOR)
            else:
                self.__gameDisplay.fill(BG_COLOR)
            self.__displayBoard()
            pygame.display.update()
            pygame.time.wait(300)
    
    def __playLevel(self, level):
        self.__board.newLevel(level)
        
        self.setBackgroundImage()
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
                    return QUIT_PROGRAM
                elif event.type == MOUSEMOTION:
                    self.__mouseX, self.__mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    self.__mouseX, self.__mouseY = event.pos
                    self.__mouseClicked = True
                elif event.type == pygame.USEREVENT or (event.type == KEYUP and event.key == K_RIGHT):
                    self.__playlist.nextSong()
                elif event.type == SoundCue.SOUND_CUE_END_EVENT:
                    self.__playlist.fadeIn() 
                    
            self.setBackgroundImage()
            self.__displayInfo(timePassed, nrMoves, level)
            
            functionResult = self.__pacaneleScreen.displayContent(self.__mouseX, self.__mouseY, self.__mouseClicked, self.__money)
            if functionResult == QUIT_PROGRAM:
                return QUIT_PROGRAM
            self.__money = functionResult
            
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
                                #if nrRevealed == 2: 
                                    return

                                if image1 in self.__imageRepo.imageSoundCues.keys():
                                    SoundCue(self.__imageRepo.imageSoundCues[image1]).play(3.0)
                                
                            firstBox = None
                            
            self.__showMouseCursor()
            pygame.display.update()
            self.__clock.tick(FPS)
            
            timePassed += self.__clock.get_time()
            self.__totalTime += self.__clock.get_time()
    
    def displayContent(self):
        for level in range(1, NR_OF_LEVELS + 1):        # level indexing starts at 1
            levelResult = self.__playLevel(level)
            if levelResult == QUIT_PROGRAM:
                return (QUIT_PROGRAM, QUIT_PROGRAM)
            
            if level == NR_OF_LEVELS:
                SoundCue(INTELIGENT_SOUND_PATH).play(3.0)
            else:
                SoundCue(SERGHEI_SOUND_PATH).play(1.0)
            
            self.__endLevelAnimation()
            pygame.time.wait(2500)
            
        return (self.__totalTime, self.__totalMoves)

