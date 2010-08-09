#! /usr/bin/python

import pygame, sys, os
from pygame.locals import *
from pygame import Color
from pygame.time import Clock

from pympd import Pympd
from pyn64 import Pyn64

class Theater():
    def __init__(self, mode):
        pygame.init()
        self.screen = pygame.display.set_mode(mode,pygame.FULLSCREEN)

        #Init Joystick
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        #Init Clock
        self.clock = Clock()

        self.applets = []
        self.applets.append(Pympd((60,60),(640,480)))
        self.applets.append(Pyn64((60,60),(640,480),'snes/'))

        self.activeAppletNumber = 0
        self.activeApplet = self.applets[0]

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            #R&L for applet change
            elif event.type == 10 and event.button in (6,7):
                if event.button == 6: #L
                    self.activeAppletNumber = ((self.activeAppletNumber+1) % 
                                                len(self.applets)) 
                if event.button == 7: #R
                    self.activeAppletNumber = ((self.activeAppletNumber+1) %
                                                len(self.applets))
                self.activeApplet= self.applets[self.activeAppletNumber]
            else:
                self.activeApplet.handle_events(event)

    def __draw(self):
        self.screen.fill(Color('black'))

        self.activeApplet.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while 1:
            self.__draw()
            self.__handle_events()
            self.clock.tick(12)




if __name__ == '__main__':
    instance = Theater(mode=(800,600))
    instance.run()
