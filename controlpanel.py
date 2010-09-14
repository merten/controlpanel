#! /usr/bin/python

import pygame, sys, os
from pygame.locals import *
from pygame import Color
from pygame.time import Clock

from modules.pympd import PyMpd
from modules.pyemu import PyEmu

from settings import *
from settings.main import *
from keys import JOYSTICK, N64Keys 

from helper import keyActions

class Theater():
    def __init__(self, mode):
        pygame.init()
        self.screen = pygame.display.set_mode(mode,pygame.FULLSCREEN)

        pygame.mouse.set_visible(False)

        #Init Joystick
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
        except pygame.error:
            print 'No joystick found'
        else:
            self.joystick.init()

        #Init Clock
        self.clock = Clock()

        #Init Applets
        self.applets = []
        self.applets.append(PyMpd((60,60),(640,480)))
        self.applets.append(PyEmu((60,60),(640,480),'media/roms/'))
        self.applets[1].set_mpdClient(self.applets[0].get_mpdClient())

        self.activeAppletNumber = 0
        self.activeApplet = self.applets[0]

        #R&L Button
        self.__leftImage = pygame.image.load("media/l.png")
        self.__rightImage = pygame.image.load("media/r.png")

        #Define actions for helper function
        self.actions = {
            "prev" : self.prevApplet,
            "next" : self.nextApplet
            }

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            #R&L for applet change
            elif keyActions(event, JOYSTICK_ACTIONS, KEYBOARD_ACTIONS, self.actions):
                self.activeApplet= self.applets[self.activeAppletNumber]
            else:
                self.activeApplet.handle_events(event)

    def __draw(self):
        self.screen.fill(Color('black'))
        
        self.activeApplet.draw(self.screen)

        halfHeight = self.screen.get_size()[1]/2 - 32

        pygame.display.flip()

    def run(self):
        while 1:
            self.__draw()
            self.__handle_events()
            self.clock.tick(12)

    def prevApplet(self):
        self.activeAppletNumber = ((self.activeAppletNumber+1) % len(self.applets))

    def nextApplet(self):
        self.activeAppletNumber = ((self.activeAppletNumber+1) % len(self.applets))


if __name__ == '__main__':
    instance = Theater(mode=(800,600))
    instance.run()
