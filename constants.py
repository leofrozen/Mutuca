    
# -*- coding: UTF-8 -*-



# Controls
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

UP_LEFT = "UP_LEFT"
UP_RIGHT = "UP_RIGHT"
DOWN_LEFT = "DOWN_LEFT"
DOWN_RIGHT = "DOWN_RIGHT"


# Define as cores
BRIGHT_RED = (255, 0, 0)
RED = (200, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
GREEN = (0, 200, 0)
BRIGHT_BLUE = (0, 0, 255)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (247, 41, 234)
YELLOW = (230, 255, 0)
GRAY = (200, 200, 200)
ORANGE = (250, 230, 0)


def get_gamelvl():
    global GAMELEVEL_NUM
    if GAMELEVEL_NUM == 0:
        GAMELEVEL = "MEDIUM"
    elif GAMELEVEL_NUM == 1:
        GAMELEVEL = "HARD"
    elif GAMELEVEL_NUM == 2:
        GAMELEVEL = "INSANITY"
    
    return GAMELEVEL

# Game levels [0, 1, 2]
GAMELEVEL_NUM = 0
GAMELEVEL = get_gamelvl()

    
# maximum size
#SCREEN_SIZE = (960,540)

# default size
#SCREEN_SIZE = (640,480)
