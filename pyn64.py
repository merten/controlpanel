#! /usr/bin/python
import pygame, sys, os
from pygame.locals import *
from pygame import Color

from controls.button import Button
from controls.list import ScrollList

from data.dirlist import DirList

from settings import *

LISTPOS = ((40,100),(600,340))

class Pyn64():
    def __init__(self, position, size, dir):

        self.surface = pygame.Surface(size)
        self.position = position

        self.dir = '%s/%s' % (os.getcwd(),dir)

        """List"""
        self.list = ScrollList(self.surface, pygame.Rect(LISTPOS))
        self.dirList = DirList(dir)
        self.list.set(self.dirList)

        
    def handle_events(self, event):
        #Joypad Button down
        if event.type == 10 and event.button in KEYMAP:

            if KEYMAP[event.button] == "A":
                self.__startGame()    
            else: #let the list handle the event
                self.list.handle_event(event)
                return

    def __startGame(self):
        game = self.dirList.getList()[self.dirList.selected]
        print 'Starting Game: ', self.dir+game
        pygame.quit()
        os.execlp('zsnes','-m',self.dir+game)
        sys.exit(0)

    def draw(self, surface):
        self.surface.fill(Color("black"))
            
        self.list.draw()

        surface.blit(self.surface, self.position)
