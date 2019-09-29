from constants import BOARD_HEIGHT, BOARD_WIDTH, BOX_SIZE, GAP_SIZE, X_MARGIN, Y_MARGIN
from images import ALL_IMAGES

def generateBoxesState(val):
    revealedBoxes = []
    for i in range(BOARD_WIDTH):
        revealedBoxes.append([val] * BOARD_HEIGHT)
    return revealedBoxes

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

def getImage(board, boxx, boxy):
    return board[boxx][boxy]

def sanityChecks():
    assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
    assert len(ALL_IMAGES) >= BOARD_HEIGHT * BOARD_WIDTH / 2, 'Not enough pictures'
    
    #if this happens, I need to do sth like this:
    #image = pygame.transform.scale(image, (BOX_SIZE, BOX_SIZE))
    #but I want to be notified if/when this happens, so I'll use assert for now
    for img in ALL_IMAGES.values():
        assert(img.get_size() == (BOX_SIZE, BOX_SIZE)), 'The image size is incorrect'
        
def convertTime(ms):
    minutes = ms / 60000
    ms %= 60000
    seconds = ms / 1000
    ms %= 1000
    return ("%02d:%02d:%03d" % (minutes, seconds, ms))