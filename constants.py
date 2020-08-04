class Constants:
    APP_TITLE = "Memorie, ba"
    FPS = 60
    
    ### DIMENSIONS ###
    WINDOW_WIDTH = 1536
    WINDOW_HEIGHT = 864
    
    ### COLORS ###
    GRAY     = (100, 100, 100)
    NAVY_BLUE = ( 60,  60, 100)
    AQUAMARINE_BLUE = (26, 44, 87)
    WHITE    = (255, 255, 255)
    BLACK    = (  0,   0,   0)
    BLUE     = (  0,   0, 255)
    ORANGE   = (255, 128,   0)
    LIGHT_ORANGE = (255, 191, 15)
    RED = (145, 0, 0)
    NAVY_RED = (104, 16, 19)
    GOLD = (235, 202, 106)
    PALE_GOLD = (209, 166, 131)
    DARK_GREEN = (35, 66, 45)
    NORMAL_GREEN = (40, 178, 75)
    
    ### VOLUME ###
    NORMAL_VOLUME = 0.25
    MIN_SOUND_CUE_VOLUME = 0.2
    VOLUME_INCREMENT = 0.01
    MAX_SOUND_CUE_VOLUME = 0.6
    
    ### DIFFICULTY ###
    NUMBER_OF_DIFFICULTIES = 3
    EASY_DIFFICULTY_MULTIPLIER = 1.0
    MEDIUM_DIFFICULTY_MULTIPLIER = 1.5
    HARD_DIFFICULTY_MULTIPLIER = 2.0
    
    COMPLETED_ACHIEVEMENT_DISPLAY_TIME = 1500 # in ms
    
    ### STAT + ACHIEVEMENT TRIGGERS ###
    TRIGGER_REVEALED_IMAGE = "revealedImage"
    TRIGGER_FOUND_IMAGE = "foundImage"
    TRIGGER_FOUND_WRONG_IMAGE = "foundWrongImage"
    TRIGGER_FOUND_SOUND_CUE = "foundSoundCue"
    TRIGGER_BOUGHT_DRINK = "boughtDrink"
    TRIGGER_MADE_BET = "betting"
    TRIGGER_END_LEVEL = "endLevel"
    TRIGGER_EXIT_LEVEL = "exitLevel"
    TRIGGER_START_GAME = "startGame"
    TRIGGER_FINISH_GAME = "endGame"
    TRIGGER_FOUND_COMBO = "foundCombo"
    TRIGGER_SET_NAME = "setName"
    TRIGGER_EARNED_MONEY = "earnedMoney"
    TRIGGER_SPENT_MONEY = "spentMoney"
    
    def __init__(self):
        pass

