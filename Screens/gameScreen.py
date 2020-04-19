from Screens.screen import Screen
import pygame
from pygame.constants import QUIT, KEYUP, K_ESCAPE, MOUSEMOTION, MOUSEBUTTONUP, K_RIGHT
from constants import BG_COLOR, FPS, BOX_COLOR, HIGHLIGHT_BORDER_SIZE, HIGHLIGHT_COLOR, LIGHT_ORANGE,\
    TEXT_LEFT_MARGIN, TEXT_TOP_MARGIN, WINDOW_HEIGHT, WINDOW_WIDTH, TEXT_COLOR, TEXT_ROW_HEIGHT,\
    TEXT_FONT, TEXT_FONT_SIZE, LIGHT_BG_COLOR, BOX_SIZE, GAP_SIZE
from board import Board, random
from Screens.pacaneleScreen import PacaneleScreen
from soundCue import SoundCue
from text import Text
from button import Button
import os

class GameScreen(Screen):
    MOUSE_CURSOR_1 = "MOUSE_CURSOR1.jpg"
    INTELIGENT_SOUND_PATH = "Music//INTELIGENT_1.ogg"
    SERGHEI_SOUND_PATH = "Music//SERGHEI_RAS.ogg"
    #BOX_REVEAL_SPEED = 360 // FPS
    BOX_REVEAL_SPEED = 3
    NR_REVEALED_BOXES = 10
    NR_OF_LEVELS = 3
    END_LEVEL_FLASH_COUNT = 10
    INCREASE_MONEY_AMOUNT = 0.1
    LEFT_MARGIN = int((WINDOW_WIDTH - (Board.BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
    TOP_MARGIN = int((WINDOW_HEIGHT - (Board.BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)
    
    MUSIC_PLAYER_BUTTON_TOP = TOP_MARGIN + 5 * TEXT_ROW_HEIGHT
    MUSIC_PLAYER_BUTTON_LEFT = TEXT_LEFT_MARGIN
    MUSIC_PLAYER_BUTTON_SIZE = TEXT_FONT_SIZE
    MUSIC_PLAYER_BUTTON_GAP_SIZE = 5
    
    def __init__(self, gameDisplay, playlist):
        self.__gameDisplay = gameDisplay
        self.__playlist = playlist
        
        self.__board = Board()
        self.__clock = pygame.time.Clock()
        self.__pacaneleScreen = PacaneleScreen(self.__gameDisplay, self.__playlist)
        
        self.__mouseX = 0
        self.__mouseY = 0
        self.__mouseClicked = False
        self.__mouseCursorImage = self.__loadSpecialImage(GameScreen.MOUSE_CURSOR_1)
        
        self.__totalMoves = 0
        self.__totalTime = 0
        self.__money = 0.0
        
    def setBackgroundImage(self):
        self.__gameDisplay.fill(BG_COLOR)
    
    def setBackgroundMusic(self):
        pass
    
    def __loadSpecialImage(self, imageTitle):
        currentImage = os.path.join(os.getcwd(), "Images")
        currentImage = os.path.join(currentImage, "Special images")
        return pygame.image.load(os.path.join(currentImage, imageTitle))
    
    def __getTopLeftCoords(self, i, j):
        top = GameScreen.TOP_MARGIN + i * (BOX_SIZE + GAP_SIZE)
        left = GameScreen.LEFT_MARGIN + j * (BOX_SIZE + GAP_SIZE)
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
                    currentObject = self.__gameDisplay.blit(self.__board.getImage(i, j).imageObject, (left, top))
                else:
                    currentObject = pygame.draw.rect(self.__gameDisplay, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE)) 
                pygame.display.update(currentObject)
    
    def __displayBoxCoverage(self, boxList, coverage, fullyCovered = False):
        for box in boxList:
            (top, left) = self.__getTopLeftCoords(box[0], box[1])
            if fullyCovered == False:
                self.__gameDisplay.blit(self.__board.getImage(box[0], box[1]).imageObject, (left, top))
            if coverage > 0:
                pygame.draw.rect(self.__gameDisplay, BOX_COLOR, (left, top, coverage, BOX_SIZE)) 
        pygame.display.update() 
        self.__clock.tick(FPS)
    
    def __revealBoxesAnimation(self, boxList):
        for coverage in range(BOX_SIZE, -1, -GameScreen.BOX_REVEAL_SPEED):
            self.__displayBoxCoverage(boxList, coverage)
        self.__displayBoxCoverage(boxList, 0)
            
    def __coverBoxesAnimation(self, boxList):
        for coverage in range(0, BOX_SIZE + 1, GameScreen.BOX_REVEAL_SPEED):
            self.__displayBoxCoverage(boxList, coverage)
        self.__displayBoxCoverage(boxList, BOX_SIZE, True)
    
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
    
    def __matchImages(self, image1, image2):
        if image1.title == image2.title:
            return True
        
        for specialPair in self.__board.specialPairs:
            if specialPair == (image1, image2) or specialPair == (image2, image1):
                return True
            
        return False
    
    def __showMouseCursor(self):
        self.__gameDisplay.blit(self.__mouseCursorImage, (self.__mouseX, self.__mouseY))
    
    def __convertTime(self, ms):
        minutes = ms / 60000
        ms %= 60000
        seconds = ms / 1000
        ms %= 1000
        return ("%02d:%02d:%03d" % (minutes, seconds, ms))  
    
    def __displayGameInfo(self, timePassed, nrMoves, level):
        Text(("Current moves = %d" % nrMoves), TEXT_FONT, TEXT_FONT_SIZE, TEXT_COLOR).display(self.__gameDisplay, TEXT_TOP_MARGIN, TEXT_LEFT_MARGIN)
        Text(("Total moves = %d" % self.__totalMoves), TEXT_FONT, TEXT_FONT_SIZE, TEXT_COLOR).display(self.__gameDisplay, TEXT_TOP_MARGIN + TEXT_ROW_HEIGHT, TEXT_LEFT_MARGIN)
        Text(("%.2f lei" % self.__money), TEXT_FONT, TEXT_FONT_SIZE, TEXT_COLOR).display(self.__gameDisplay, TEXT_TOP_MARGIN + 2 * TEXT_ROW_HEIGHT, TEXT_LEFT_MARGIN)
        Text(("Level = %d / %d" % (level, GameScreen.NR_OF_LEVELS)), TEXT_FONT, TEXT_FONT_SIZE, TEXT_COLOR).display(self.__gameDisplay, TEXT_TOP_MARGIN + 3 * TEXT_ROW_HEIGHT, TEXT_LEFT_MARGIN)
        Text(self.__convertTime(timePassed), TEXT_FONT, TEXT_FONT_SIZE, TEXT_COLOR).display(self.__gameDisplay, WINDOW_HEIGHT - 2 * TEXT_ROW_HEIGHT - TEXT_TOP_MARGIN, TEXT_LEFT_MARGIN)
        Text(self.__convertTime(self.__totalTime), TEXT_FONT, TEXT_FONT_SIZE, TEXT_COLOR).display(self.__gameDisplay, WINDOW_HEIGHT - TEXT_ROW_HEIGHT - TEXT_TOP_MARGIN, TEXT_LEFT_MARGIN)
            
    def __endLevelAnimation(self):
        for i in range(GameScreen.END_LEVEL_FLASH_COUNT):
            if i % 2 == 0:
                self.__gameDisplay.fill(LIGHT_BG_COLOR)
            else:
                self.__gameDisplay.fill(BG_COLOR)
            self.__displayBoard()
            pygame.display.update()
            pygame.time.wait(300)
    
    def __displayPacaneleButton(self):
        pacaneleButtonText = Text("Dubleaza", TEXT_FONT, TEXT_FONT_SIZE, LIGHT_ORANGE)
        pacaneleButton = Button(PacaneleScreen.DOUBLE_MONEY_BOX_TOP, PacaneleScreen.DOUBLE_MONEY_BOX_LEFT, PacaneleScreen.DOUBLE_MONEY_BOX_WIDTH, TEXT_ROW_HEIGHT, LIGHT_BG_COLOR, pacaneleButtonText)
        pacaneleButton.display(self.__gameDisplay)
        
        if pacaneleButton.collides(self.__mouseX, self.__mouseY):
            pacaneleButton.drawHighlight(self.__gameDisplay, HIGHLIGHT_COLOR, HIGHLIGHT_BORDER_SIZE)
            if self.__mouseClicked and self.__money > 0.0:
                functionResult = self.__pacaneleScreen.displayContent(self.__money)
                if functionResult == Screen.QUIT_PROGRAM:
                    return Screen.QUIT_PROGRAM
                self.__money = functionResult
                
    def __displayMusicPlayer(self):
        previousSongButtonText = Text("<", TEXT_FONT, TEXT_FONT_SIZE, LIGHT_ORANGE)
        previousSongButton = Button(GameScreen.MUSIC_PLAYER_BUTTON_TOP, GameScreen.MUSIC_PLAYER_BUTTON_LEFT, GameScreen.MUSIC_PLAYER_BUTTON_SIZE, GameScreen.MUSIC_PLAYER_BUTTON_SIZE, LIGHT_BG_COLOR, previousSongButtonText)
        previousSongButton.display(self.__gameDisplay)
        
        if previousSongButton.collides(self.__mouseX, self.__mouseY) and self.__mouseClicked:
            self.__playlist.previousSong()
            
        pauseSongButtonText = Text("||", TEXT_FONT, TEXT_FONT_SIZE, LIGHT_ORANGE)
        pauseSongButton = Button(GameScreen.MUSIC_PLAYER_BUTTON_TOP, GameScreen.MUSIC_PLAYER_BUTTON_LEFT + GameScreen.MUSIC_PLAYER_BUTTON_GAP_SIZE + GameScreen.MUSIC_PLAYER_BUTTON_SIZE, GameScreen.MUSIC_PLAYER_BUTTON_SIZE, GameScreen.MUSIC_PLAYER_BUTTON_SIZE, LIGHT_BG_COLOR, pauseSongButtonText)
        pauseSongButton.display(self.__gameDisplay)
        
        if pauseSongButton.collides(self.__mouseX, self.__mouseY) and self.__mouseClicked:
            self.__playlist.pauseButtonAction()
            
        nextSongButtonText = Text(">", TEXT_FONT, TEXT_FONT_SIZE, LIGHT_ORANGE)
        nextSongButton = Button(GameScreen.MUSIC_PLAYER_BUTTON_TOP, GameScreen.MUSIC_PLAYER_BUTTON_LEFT + 2 * GameScreen.MUSIC_PLAYER_BUTTON_GAP_SIZE + 2 * GameScreen.MUSIC_PLAYER_BUTTON_SIZE, GameScreen.MUSIC_PLAYER_BUTTON_SIZE, GameScreen.MUSIC_PLAYER_BUTTON_SIZE, LIGHT_BG_COLOR, nextSongButtonText)
        nextSongButton.display(self.__gameDisplay)
        
        if nextSongButton.collides(self.__mouseX, self.__mouseY) and self.__mouseClicked:
            self.__playlist.nextSong()
        
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
            self.__mouseClicked = False
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    return Screen.QUIT_PROGRAM
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
            self.__displayGameInfo(timePassed, nrMoves, level)
            self.__displayMusicPlayer()
            pacaneleResult = self.__displayPacaneleButton()
            if pacaneleResult == Screen.QUIT_PROGRAM:
                return Screen.QUIT_PROGRAM
            
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
                            
                            if self.__matchImages(image1, image2):
                                nrRevealed += 2
                                self.__money += GameScreen.INCREASE_MONEY_AMOUNT
                                
                                if nrRevealed == self.__board.height * self.__board.width:  
                                #if nrRevealed == 2: 
                                    return

                                if image1.soundCue != None:
                                    SoundCue(image1.soundCue).play(3.0)
                            
                            else:
                                pygame.time.wait(1000)
                                self.__coverBoxesAnimation([(firstBox[0], firstBox[1]), (xBox, yBox)])
                                self.__board.coverBox(firstBox[0], firstBox[1])
                                self.__board.coverBox(xBox, yBox)
                                
                            firstBox = None
                            
            self.__showMouseCursor()
            pygame.display.update()
            self.__clock.tick(FPS)
            
            timePassed += self.__clock.get_time()
            self.__totalTime += self.__clock.get_time()
    
    def displayContent(self):
        for level in range(1, GameScreen.NR_OF_LEVELS + 1):        # level indexing starts at 1
            levelResult = self.__playLevel(level)
            if levelResult == Screen.QUIT_PROGRAM:
                return (Screen.QUIT_PROGRAM, Screen.QUIT_PROGRAM)
            
            if level == GameScreen.NR_OF_LEVELS:
                SoundCue(GameScreen.INTELIGENT_SOUND_PATH).play(3.0)
            else:
                SoundCue(GameScreen.SERGHEI_SOUND_PATH).play(1.0)
            
            self.__endLevelAnimation()
            pygame.time.wait(2500)
            
        return (self.__totalTime, self.__totalMoves)

