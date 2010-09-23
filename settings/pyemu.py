"""
PyEmu Module Settings
updated 16/09/2010
"""

from pygame.locals import *
from keys import N64Keys


# GUI Settings

LISTPOS = ((40,100),(600,340))

ENDINGS = (".zip",".smc",".rar",".rom")

LOGO = "media/nintendo_snes_small.png"

# Key Definitions
JOYSTICK_ACTIONS = {
    N64Keys.A : "start_game"
}

KEYBOARD_ACTIONS = {
    K_RETURN : "start_game"
}

# Emulator Settings
EMULATOR="zsnes"
EMULATOR_ARGS="-m"