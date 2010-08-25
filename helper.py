########################
#                      #
# Helper functions     #
#                      #
########################

from pygame.locals import *

from keys import JOYSTICK

'''
Runs an action if current event is in keytable.
@param actions table of actions and keywords.
@return False if no action was found otherwise True
'''
def keyActions(event, joystick_actions, keyboard_actions, actions):
    if event.type == JOYSTICK and event.button in joystick_actions:
        if joystick_actions[event.button] in actions:
            actions[joystick_actions[event.button]]()
            return True
    elif event.type == KEYDOWN and event.key in keyboard_actions:
        if keyboard_actions[event.key] in actions:
            actions[keyboard_actions[event.key]]()
            return True    
    return False
