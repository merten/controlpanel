"""
GUI element for displaying selectable lists.
"""
import pygame
from pygame import Surface, Color
from pygame.locals import *

from settings.main import *
from settings.list import *
#from keys import JOYSTICK

from helper import keyActions

class ScrollList():
    """
    Displays a list that implements the selectable list.
    """
    def __init__(self, surface, rect):
        """
        Args:
            surface: The Surface to draw the List on.
            rect: The position and dimensions of the List on the
                    target surface.
        """
        self.dest = surface
        self.position = rect
        self.width, self.height = self.position.size
        
        self.elementsPerPage = self.height / LIST_ELEM_HEIGHT
        self.elementSize = (self.width-LIST_SCROLLBAR_WIDTH, LIST_ELEM_HEIGHT)
        
        self.surface = pygame.Surface(self.position.size)
        
        self.list = None
        self.drawList = []
        self.update = True

        self.begin = 0

        #key Actions
        self.actions = {
            "down"  : self.__down,
            "up"    : self.__up
            }
        
    def set(self, list):
        """
        Set new selectable list to print.
        """
        if self.list.getList() == list.getList():
            return

        self.list = list

        self.drawList = [ ListElement(unicode(element), self.elementSize) for element in list.getList() ]

        self.update = True
            
    def handle_event(self, event):
        """
        Handle the event not handled by the GUI.
        """
        keyActions(event,JOYSTICK_ACTIONS, KEYBOARD_ACTIONS, self.actions) 
    
    def draw(self):
        """
        Draw the List object onto the surface.
        """
        if self.update:
            self.surface.fill(pygame.Color(LIST_BGCOLOR))
            
                                                     
            #print list \w selected element
            #set begin
            if len(self.list) <= self.elementsPerPage:
                self.begin = 0
            elif self.list.selected > self.begin + self.elementsPerPage -1:
                self.begin = self.list.selected - self.elementsPerPage +1
            elif self.list.selected < self.begin:
                self.begin = self.list.selected
            
            #print list elements
            for i, element in enumerate(self.drawList[self.begin:(self.begin + self.elementsPerPage)]):
                if i + self.begin == self.list.selected:
                    drawElement = element.getSelectedSurface()
                elif i + self.begin == self.list.playing:
                    drawElement = element.getCurrentSurface()
                else:
                    drawElement = element.getSurface()           

                self.surface.blit(drawElement,
                                  (0,i*LIST_ELEM_HEIGHT))

            #print scrollbar
            pygame.draw.rect(self.surface,
                             pygame.Color(LIST_SCROLLBAR_COLOR),
                             pygame.Rect((self.position.width - LIST_SCROLLBAR_WIDTH,
                                         self.__get_scroll_position()), 
                                         (LIST_SCROLLBAR_WIDTH, self.__get_scroll_height())))

            
            self.update = False
                         
        #copy to destination
        self.dest.blit(self.surface,
                       self.position)

    def __up(self):
        """
        Moves the selection up.
        """
        if len(self.list) != 0:
            self.list.selected = (self.list.selected-1) % len(self.list)
            self.update = True

    def __down(self):
        """
        Moves the selection down.
        """
        if len(self.list) != 0:
            self.list.selected = (self.list.selected+1) % len(self.list)
            self.update = True

    def __get_scroll_position(self):
        """
        Returns: 
            The (upper) scrollbar position based on the current list position.
        """
        if self.begin == 0:
            return 0
        else:
            #correct end
            return (((self.height - self.__get_scroll_height()) * self.begin) /
                (len(self.list)  - self.elementsPerPage))

    def __get_scroll_height(self):
        """
        Returns the current scrollbar height based on number of elements.
        """
        if len(self.list) <= self.elementsPerPage:
            return self.height
        else:
            return (self.elementsPerPage * self.height) / len(self.list)
        


class ListElement:
    def __init__(self, caption, size):
        """
        Args:
            caption: Text on the new element.
            size: Size of the new element surface. Tuple of width and height.
        """
        self.caption = caption
        self.surface = pygame.Surface(size)
        self.selectedSurface = pygame.Surface(size)
        self.currentSurface = pygame.Surface(size)
        
        self.surface = None;

    def updateSurface(self):
        """
        Update all list element surfaces.
        """
        #render normal list element
        self.surface.fill(Color(LIST_ELEM_BGCOLOR))
        
        font = pygame.font.Font(pygame.font.get_default_font(), self.surface.get_size()[1] - 2)
        fontSurface = font.render(self.caption,
                                  True,
                                  Color(LIST_ELEM_TEXTCOLOR),
                                  Color(LIST_ELEM_BGCOLOR))
        self.surface.blit(fontSurface, (0,0))
        
        #render selected list element
        self.selectedSurface.fill(Color(LIST_ELEM_BGCOLOR_SELECTED))
        
        font = pygame.font.Font(pygame.font.get_default_font(), self.selectedSurface.get_size()[1] - 2)
        fontSurface = font.render(self.caption,
                                  True,
                                  Color(LIST_ELEM_TEXTCOLOR),
                                  Color(LIST_ELEM_BGCOLOR_SELECTED))
        self.selectedSurface.blit(fontSurface, (0,0))

        #render current list element
        self.currentSurface.fill(Color(LIST_ELEM_BGCOLOR_CURRENT))

        font = pygame.font.Font(pygame.font.get_default_font(),
                                self.currentSurface.get_size()[1]-2)
        fontSurface = font.render(self.caption,
                                  True,
                                  Color(LIST_ELEM_TEXTCOLOR),
                                  Color(LIST_ELEM_BGCOLOR_CURRENT))
        self.currentSurface.blit(fontSurface, (0,0))

    def getSurface(self):
        """
        Returns:
            The unselected Surface.
        """
        if self.surface == None:
            self.updateSurface()
        return self.surface

    def getSelectedSurface(self):
        """
        Returns:
            The selected Surface.
        """
        return self.selectedSurface

    def getCurrentSurface(self):
        """
        Returns:
            The current marked Surface.
        """
        return self.currentSurface
