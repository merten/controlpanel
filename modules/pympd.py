# -*- coding: utf-8
"""
This is the applet to control the MPD daemon via the  controlpanel interface.
"""
import pygame, sys, os
from pygame import Color

from mpd import (MPDClient, CommandError, ConnectionError, ProtocolError)

from controls.button import Button
from controls.list import ScrollList
from data.dataCollector import DataCollector, MpdNotConnected
from data.playlist import Playlist

from settings.pympd import *
from helper import keyActions


def mpdAccess(fun):
    """
    Decorator that allows functions to access the remote server only if a
    connection exists.
    """
    def mpdDecorator(*args):
        if args[0].connected:
            fun(*args) 
    return mpdDecorator

class PyMpd():
    def __init__(self, panel, position, size):
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

        self.__mpdClient = DataCollector(HOST, PORT)
        self.connected = self.__mpdClient.connected

        # Retrieve current status.
        self.__updateDataCollector()
        self.__updateButtons()

        if self.connected:
            self.__mpdClient.unmute()
            
        self.__notify = ""

        #key actions
        self.actions = {
            "play"  : self.__mpdClient.play,
            "stop"  : self.__mpdClient.stop,
            "prev"  : self.__mpdClient.previous,
            "next"  : self.__mpdClient.next,
            "delete": self.__mpdClient.delete,
            "volume_up"   : self.__mpdClient.volume_up,
            "volume_down" : self.__mpdClient.volume_down
            }

    def get_mpdClient(self):
        """
        Returns:
            The data collector interface for controll with other classes.
        """
        return self.__mpdClient

    @mpdAccess
    def handle_events(self, event):
        #Joypad Button down
        if event.type == USEREVENT+1:
            self.__updateDataCollector
        elif not keyActions(event, JOYSTICK_ACTIONS, KEYBOARD_ACTIONS, self.actions):
            #let the list handle the event
            self.list.handle_event(event)
            return

        self.__updateDataCollector()
        self.__updateButtons()

    '''
    Update dataCollector.
    '''
    @mpdAccess
    def __updateDataCollector(self):
        """
        Updates the status and the playlist of the MPD server.
        """
        self.__mpdClient.updateStatus()
        self.__mpdClient.updatePlaylist()
        self.__updatePlaylist()
        
        #Update notification area
        if self.__mpdClient.status.state in ("play", "pause"):
            self.__notify = u"Lautstärke: %s %%" % self.__mpdClient.status.volume
        else:
            self.__notify = ""
             
    '''
    Set local playlist to server playlist.
    '''
    @mpdAccess
    def __updatePlaylist(self):
        self.list.set(self.__mpdClient.getPlaylist())

    @mpdAccess
    def __updateButtons(self):
        """
        Updates all buttons according to their state in the MPD daemon.
        """
        self.__mpdClient.updateStatus()
        for button in self.buttons.values():
            button.active = False

        state = self.__mpdClient.status.state

        if state == 'play':
            self.buttons['play'].active = True
        if state == 'stop':
            self.buttons['stop'].active = True
        if state == 'pause':
            self.buttons['pause'].active = True

                
    def draw(self, surface):
        self.panel.notify(self.__notify)
        
        self.surface.fill(Color("black"))
        
        for button in self.buttons.values():
            button.draw(self.surface)
            
        self.list.draw()

        surface.blit(self.surface, self.position)