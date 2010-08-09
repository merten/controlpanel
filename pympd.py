#! /usr/bin/python
import pygame, sys, os
from pygame.locals import *
from pygame import Color

from mpd import (MPDClient, CommandError, ConnectionError, ProtocolError)
#from socket import error as SocketError

from controls.button import Button
from controls.list import ScrollList
from data.dataCollector import DataCollector, MpdNotConnected
from data.playlist import Playlist

from settings import *



BUTTONS = [
    {"name":"pause", "active":"media/pause-active.png", "inactive":"media/pause.png", "position":(148,20)},
    {"name":"play", "active":"media/play-active.png", "inactive":"media/play.png", "position":(218,20)},
    {"name":"stop", "active":"media/stop-active.png", "inactive":"media/stop.png", "position":(288,20)},
    {"name":"rew", "active":"media/rew-active.png", "inactive":"media/rew.png", "position":(358,20)},
    {"name":"ff", "active":"media/ff-active.png", "inactive":"media/ff.png", "position":(428,20)},
]

LISTPOS = ((40,100),(600,340))

'''
Decorator
'''
def mpdAccess(fun):
    def decorator(*args):
        if args[0].connected:
            fun(*args) 
    return decorator

class Pympd():
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

    @mpdAccess
    def handle_events(self, event):
        #Joypad Button down
        if event.type == USEREVENT+1:
            self.__updateDataCollector
        elif event.type == 10 and event.button in KEYMAP:

            if KEYMAP[event.button] == "A":
                self.__mpdClient.play()    
            elif KEYMAP[event.button] == "B":
                self.__mpdClient.stop()
            elif KEYMAP[event.button] == "left":
                self.__mpdClient.previous()
            elif KEYMAP[event.button] == "right":
                self.__mpdClient.next()
            elif KEYMAP[event.button] == "c-right":
                self.__mpdClient.delete()
            else: #let the list handle the event
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
            
        
