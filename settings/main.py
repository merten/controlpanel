"""
Main Module Settings
updated 16/09/2010
"""

from pygame.locals import *
from keys import N64Keys

# General Settings


# GUI Settings
LIST_BGCOLOR = "white"
LIST_ELEM_HEIGHT = 20
LIST_ELEM_BGCOLOR = "white"
LIST_ELEM_BGCOLOR_SELECTED = "red"
LIST_ELEM_BGCOLOR_CURRENT = "orange"
LIST_ELEM_TEXTCOLOR = "black"
LIST_SCROLLBAR_WIDTH = 13
LIST_SCROLLBAR_COLOR = "blue"

NOTIFY_FONT_COLOR = "white"

# Key Definitions
JOYSTICK_ACTIONS = {
    N64Keys.L : "prev",
    N64Keys.R : "next"
}

KEYBOARD_ACTIONS = {
    K_TAB : "next"
}