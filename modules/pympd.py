#! /usr/bin/python
import pygame, sys, os
from pygame.locals import *
from pygame import Color

from mpd import (MPDClient, CommandError, ConnectionError, ProtocolError)

from controls.button import Button
from controls.list import ScrollList
from data.dataCollector import DataCollector, MpdNotConnected
from data.playlist import Playlist

from settings.pympd import *

from helper import keyActions


'''
Decorator
'''
def mpdAccess(fun):
    def decorator(*args):
        if args[0].connected:
            fun(*args) 
    return decorator

class PyMpd():
    def __init__(self, position, size):

        self.surface = pygame.Surface(size)
        self.position = position

        #set timer for playlist refresh
        pygame.time.set_timer(USEREVENT+1, 5000)
                
        """Buttons"""
        self.buttons = {}
        for button in BUTTONS:
            self.buttons[button["name"]] = Button(button["inactive"], button["active"] , button["position"])
            
        """List"""
        self.list = ScrollList(self.surface, pygame.Rect(LISTPOS))
        self.list.set(Playlist([]))

        self.__mpdClient = DataCollector(HOST, PORT)
        self.connected = self.__mpdClient.connected

        self.__updateDataCollector()
        self.__updateButtons()

        if self.connected:
            self.__mpdClient.unmute()

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
        self.__mpdClient.updateStatus()
        self.__mpdClient.updatePlaylist()
        self.__updatePlaylist()
           
    '''
    Set local playlist to server playlist.
    '''
    @mpdAccess
    def __updatePlaylist(self):
        self.list.set(self.__mpdClient.getPlaylist())

    '''
    Updates all buttons according to their state in the MPD daemon.
    '''
    @mpdAccess
    def __updateButtons(self):
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
        self.surface.fill(Color("black"))
        
        for button in self.buttons.values():
            button.draw(self.surface)
            
        self.list.draw()

        surface.blit(self.surface, self.position)
            
        
