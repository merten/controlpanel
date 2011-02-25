"""
This applet is the central notification area for the control panel.
"""

import pygame
from pygame import Color

from settings.main import *

class NotificationArea():
    def __init__(self, panel, position, size):
        self.position = position
        self.size = size
        self.panel = panel
        
        self.surface = pygame.Surface(size)
        
        self.caption = " "
        self.setCaption("")
        
        
    def setCaption(self, caption):
        if self.caption != caption:
            self.caption
            self.surface.fill(Color("black"))
            font = pygame.font.Font(pygame.font.get_default_font(), self.size[1] - 2)
            self.surface.blit(font.render(caption,
                              True,
                              Color(NOTIFY_FONT_COLOR)),
                              (0,1))
        
    
    def draw(self, surface):
        surface.blit(self.surface,self.position)

