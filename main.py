#! python3

'''
to add / fix:
- timer
- nr. of moves
- fix box cover, it was a problem with the original program as well
- title screen, with a different song
- fix sound fade in
'''

import random

from constants import *
from images import *
from pygame.locals import *
from music import *

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARD_WIDTH):
        revealedBoxes.append([val] * BOARD_HEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    # Get a list of every possible image.
    icons = []
    for image in ALL_IMAGES.values():
        icons.append(image)

    random.shuffle(icons) # randomize the order of the icons list
    numImagesUsed = int(BOARD_WIDTH * BOARD_HEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numImagesUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
        
    return board

def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOX_SIZE + GAP_SIZE) + X_MARGIN
    top = boxy * (BOX_SIZE + GAP_SIZE) + Y_MARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
            
    return (None, None)

def drawImage(image, boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    DISPLAY.blit(image, (left, top))

def getImage(board, boxx, boxy):
    return board[boxx][boxy]

def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAY, BG_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
        image = getImage(board, box[0], box[1])
        drawImage(image, box[0], box[1])
        
        # this is the "coverBoxAnimation" part
        if coverage > 0: 
            pygame.draw.rect(DISPLAY, BOX_COLOR, (left, top, coverage, BOX_SIZE))
            
    pygame.display.update()
    FPS_CLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED):
        drawBoxCovers(board, boxesToReveal, coverage)     

def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    # the end value is a "magic number", need to fix that
    for coverage in range(0, BOX_SIZE + 6, REVEAL_SPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAY, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                # Draw the (revealed) icon.
                image = getImage(board, boxx, boxy)
                drawImage(image, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAY, HIGHLIGHT_COLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)

def startGameAnimation(board):
    # Randomly reveal the boxes 10 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(10, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)
        
def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHT_BG_COLOR
    color2 = BG_COLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAY.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def quitGame():
    fadeOut()
    pygame.quit()
    quit()

def sanityChecks():
    assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
    assert len(ALL_IMAGES) == BOARD_HEIGHT * BOARD_WIDTH / 2, 'The number of pictures is incorrect'
    
    #if this happens, I need to do sth like this:
    #image = pygame.transform.scale(image, (BOX_SIZE, BOX_SIZE))
    #but I want to be notified if/when this happens, so I'll use assert for now
    for img in ALL_IMAGES.values():
        assert(img.get_size() == (BOX_SIZE, BOX_SIZE)), 'The image size is incorrect'

def main():
    sanityChecks()
    
    global FPS_CLOCK, DISPLAY
    
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    pygame.display.set_icon(SERGHEI_ICON1)
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    mouseX = 0
    mouseY = 0
    nrMoves = 0
    nrRevealed = 0
    
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    
    firstSelection = None
    
    DISPLAY.fill(BG_COLOR)
    playMusic()
    startGameAnimation(mainBoard)
    
    while True:
        mouseClicked = False
        
        DISPLAY.fill(BG_COLOR)
        drawBoard(mainBoard, revealedBoxes)
        
        # event handling loop 
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                quitGame()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True
        
        boxx, boxy = getBoxAtPixel(mouseX, mouseY)
        
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
                
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                    
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    image1 = getImage(mainBoard, firstSelection[0], firstSelection[1])
                    image2 = getImage(mainBoard, boxx, boxy)
                    
                    #nrMoves += 1
                    #print (nrMoves)

                    if image1 != image2:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                        
                    else:
                        nrRevealed += 2
                        
                        if nrRevealed == 2:
                            nrRevealed = 0
                            
                            playWinningSound()
                            
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)
    
                            # Reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = generateRevealedBoxesData(False)
                            
                            # Replay the start game animation.
                            startGameAnimation(mainBoard)
                                                
                    firstSelection = None # reset firstSelection variable
                    
        if pygame.mixer.Channel(1).get_busy() == 0:
            fadeIn()
                    
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
            
if __name__ == "__main__":
    main()
