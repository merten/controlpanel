#! /usr/bin/python
"""
    Controlpanel is a easy to to use control panel for the mpd music daemon
    and the zsnes Super Nintendo Emulator.
    

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
"""

import logging
import pygame, sys
from pygame import Color
from pygame.time import Clock

from modules.pympd import PyMpd
from modules.pyemu import PyEmu
from modules.pynotify import NotificationArea

from settings.main import *

from helper import keyActions

class Panel():
    def __init__(self, mode):
        self.logger = logging.getLogger('controlpanel') 
        
        self.logger.debug('Init pygame')
        pygame.init()
        self.screen = pygame.display.set_mode(mode,pygame.RESIZABLE)

        pygame.mouse.set_visible(False)

        #Init Joystick
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
        except pygame.error:
            self.logger.info('No joystick found')
        else:
            self.joystick.init()

        #Init Clock
        self.clock = Clock()
        
        #Activate notification area
        self.notificationArea = NotificationArea(self, (60,540), (640,20))

        #Init Applets
        self.applets = []
        self.applets.append(PyMpd(self, (60,60),(640,480)))
        self.applets.append(PyEmu(self, (60,60),(640,480),'media/roms/'))
        #self.applets[1].set_mpd_commander(self.applets[0].commander)

        self.activeAppletNumber = 0
        self.activeApplet = self.applets[0]

        #Define actions for helper function
        self.actions = {
            "prev" : self.prevApplet,
            "next" : self.nextApplet
            }

    def __handle_events(self):
        """ 
        Handles the waiting events, if the key is not in the classes action
        list the event is forwarded to the active applet.
        """            
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.event.clear()
                self.applets[0].exit()
                self.running = False
                break
            elif keyActions(event, JOYSTICK_ACTIONS, KEYBOARD_ACTIONS, self.actions):
                self.activeApplet= self.applets[self.activeAppletNumber]
            else:
                self.activeApplet.handle_events(event)

    def __draw(self):
        self.screen.fill(Color('black'))
        self.activeApplet.draw(self.screen)
        self.notificationArea.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.__draw()
            self.__handle_events()
            self.clock.tick(12)

        self.logger.debug('Terminating')
        pygame.quit()
        sys.exit()
    
    def notify(self, caption):
        """
        Prints a new caption to the notification area.
        """
        self.notificationArea.setCaption(caption)

    def prevApplet(self):
        """ Rotates through the applets forward. The next applet is displayed. """
        self.activeAppletNumber = ((self.activeAppletNumber+1) % len(self.applets))

    def nextApplet(self):
        """ Rotates through the applets backward. The next applet is displayed. """
        self.activeAppletNumber = ((self.activeAppletNumber+1) % len(self.applets))


if __name__ == '__main__':
    logging.basicConfig(filename=LOGGING_PATH,
                        filemode='w',
                        level=LOGGING_LEVEL,
                        format='%(asctime)s -[%(name)s-%(levelname)s]- %(message)s',
                        datefmt='%d.%m.%Y %H:%M')
    logging.getLogger().addHandler(logging.StreamHandler()) #Write to Console too
    instance = Panel(mode=(800,600))
    instance.run()
