#########################
#                       #
# Main Module Settings  #
# 25/08/2010            #
#                       #
#########################

from pygame.locals import *

from settings import *
from keys import N64Keys

JOYSTICK_ACTIONS = {
    N64Keys.L : "prev",
    N64Keys.R : "next"
}

KEYBOARD_ACTIONS = {
    K_TAB : "next"
}
