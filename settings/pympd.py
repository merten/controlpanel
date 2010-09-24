"""
PyMpd Module Settings
25/08/2010
"""

from pygame.locals import *
from keys import N64Keys

# MPD Settings
HOST = 'localhost'
PORT = '6600'
PASSWORD = False

# GUI Settings
LISTPOS = ((40,100),(600,340))

BUTTONS = [
    {"name":"pause", "active":"media/pause-active.png",
     "inactive":"media/pause.png", "position":(148,20)},
    {"name":"play", "active":"media/play-active.png",
     "inactive":"media/play.png", "position":(218,20)},
    {"name":"stop", "active":"media/stop-active.png",
     "inactive":"media/stop.png", "position":(288,20)},
    {"name":"rew", "active":"media/rew-active.png",
     "inactive":"media/rew.png", "position":(358,20)},
    {"name":"ff", "active":"media/ff-active.png", 
     "inactive":"media/ff.png", "position":(428,20)},
]

# Key Definitions
JOYSTICK_ACTIONS = {
    N64Keys.A : "play",
    N64Keys.B : "stop",
    N64Keys.LEFT    : "prev",
    N64Keys.RIGHT   : "next",
    N64Keys.C_UP    : "volume_up",
    N64Keys.C_DOWN  : "volume_down"
}

KEYBOARD_ACTIONS = {
    K_RETURN : "play",
    K_p : "stop",
    K_PLUS   : "volume_up",
    K_MINUS  : "volume_down",
}
