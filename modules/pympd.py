# -*- coding: utf-8
"""
This is the applet to control the MPD daemon via the  controlpanel interface.
"""
import pygame, sys, os
from pygame import Color
import logging

from mpd import (MPDClient, CommandError, ConnectionError, ProtocolError)

from controls.button import Button
from controls.list import ScrollList
from data.commander import Commander, CommanderThread
from data.data import Data
from data.playlist import Playlist

from settings.pympd import *
from helper import keyActions


class PyMpd():
    def __init__(self, panel, position, size):
        self.logger = logging.getLogger('controlpanel.pympd')
        self.panel = panel
    
        self.surface = pygame.Surface(size)
        self.position = position

        #Set timer for playlist refresh.
        pygame.time.set_timer(USEREVENT+1, 5000)
                
        # Init Buttons
        self.buttons = {}
        for button in BUTTONS:
            self.buttons[button["name"]] = Button(button["inactive"], button["active"] , button["position"])
            
        # Init the playlist view.
        self.list = ScrollList(self.surface, pygame.Rect(LISTPOS))
        self.list.set(Playlist([]))

        self.commander = Commander()
        self.__data = Data()
        self.__commanderThread = CommanderThread(self.commander,
						                         self.__data,
                                                 HOST, PORT)
        self.__commanderThread.start()

        # Retrieve current status.
        self.__updateData()
        self.__updateButtons()

        self.commander.unmute()
            
        self.__notify = ""

        #key actions
        self.actions = {
            "play"  : self.commander.play,
            "stop"  : self.commander.stop,
            "prev"  : self.commander.previous,
            "next"  : self.commander.next,
            "delete": self.commander.delete,
            "volume_up"   : self.commander.volume_up,
            "volume_down" : self.commander.volume_down
            }

    def exit(self):
        self.logger.debug('send exit command to MPD-client thread.')
        self.commander.exit()
        self.logger.debug('waiting for MPD-client thread.')
        while self.__commanderThread.is_alive():
            pass
        self.logger.debug('MPD-client thread terminated.')

        del self.__commanderThread
        del self.commander
        del self.__data

    def handle_events(self, event):
        #Joypad Button down
        if event.type == USEREVENT+1:
            pass
        elif not keyActions(event, JOYSTICK_ACTIONS, KEYBOARD_ACTIONS, self.actions):
            #let the list handle the event
            self.list.handle_event(event)
            return

        self.__updateData()
        self.__updateButtons()

    def __updateData(self):
        """
        Updates the status and the playlist of the MPD server.
        """
        self.commander.update_status()
        self.commander.update_playlist()
        self.__updatePlaylist()
        
        #Update notification area
        try:
            if self.__data.status.state in ("play", "pause"):
                self.__notify = u"Lautstärke: %s %%" % self.__mpdClient.status.volume
            else:
                self.__notify = ""
        except AttributeError:
            self.__notify = ""
             
    def __updatePlaylist(self):
        """
        Set local playlist to server playlist.
        """
        if self.__data.playlist:
            self.list.set(self.__data.playlist)

    def __updateButtons(self):
        """
        Updates all buttons according to their state in the MPD daemon.
        """
        for button in self.buttons.values():
            button.active = False

        try:
            state = self.__data.status.state

            if state == 'play':
                self.buttons['play'].active = True
            if state == 'stop':
                self.buttons['stop'].active = True
            if state == 'pause':
                self.buttons['pause'].active = True
        except AttributeError:
            pass

                
    def draw(self, surface):
        self.panel.notify(self.__notify)
        
        #self.surface.fill(Color("black"))
        
        for button in self.buttons.values():
            button.draw(self.surface)
            
        self.list.draw()

        surface.blit(self.surface, self.position)
