# -*- coding: utf-8
"""
This is the applet to launch and list games from the ROM-directory.
"""
import pygame, sys, os
from pygame import Color

from controls.button import Button
from controls.list import ScrollList
from data.dirlist import DirList
from settings.pyemu import *
from keys import JOYSTICK
from helper import keyActions


class PyEmu():
    def __init__(self, panel, position, size, dir):

        self.panel = panel
        
        self.__notify = "Wähle ein Spiel."
        
        self.surface = pygame.Surface(size)
        self.position = position

        self.dir = '%s/%s' % (os.getcwd(),dir)

        #List
        self.list = ScrollList(self.surface, pygame.Rect(LISTPOS))
        self.dirList = DirList(dir)
        self.list.set(self.dirList)

        #Logo
        self.logo = pygame.image.load(LOGO)
        self.logo_position = ((size[0]/2) - (self.logo.get_width()/2), 0)

        self.__mpdClient = None

        #key actions
        self.actions = {
            "start_game" : self.__startGame
            }

    def set_mpdClient(self, controller):
        self.__mpdClient = controller

        
    def handle_events(self, event):
        if not keyActions(event, JOYSTICK_ACTIONS, KEYBOARD_ACTIONS, self.actions):
            #let the list handle the event
            self.list.handle_event(event)
    

    def __startGame(self):
        game = self.dirList.getList()[self.dirList.selected]
        print 'Starting Game: ', self.dir+game

        if self.__mpdClient and self.__mpdClient.connected:
            self.__mpdClient.mute()

        pygame.quit()
        os.execlp(EMULATOR,EMULATOR_ARGS, self.dir+game)
        sys.exit(0)

    def draw(self, surface):
        self.panel.notify(self.__notify)
        
        self.surface.fill(Color("black"))
            
        self.list.draw()
        self.surface.blit(self.logo, self.logo_position)

        surface.blit(self.surface, self.position)
