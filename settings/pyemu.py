#########################
#                       #
# PyEmu Module Settings #
# 25/08/2010            #
#                       #
#########################

from pygame.locals import *

from settings import *
from keys import N64Keys

LISTPOS = ((40,100),(600,340))

LOGO = "media/nintendo_snes_small.png"

JOYSTICK_ACTIONS = {
    N64Keys.A : "start_game"
}

KEYBOARD_ACTIONS = {
    K_RETURN : "start_game"
}
