"""

 List GUI element
 modified 25.08.2010

"""
import pygame
from pygame import Surface, Color
from pygame.locals import *

from settings.list import *
from keys import JOYSTICK

from helper import keyActions

"""
GUI element.
Displays a list that implements the selectable list.
"""
class ScrollList():
    """
    Create a new list object.
    @param surface The Surface to draw the List on
    @param rect The position and dimensions of the List
    """
    def __init__(self, surface, rect):
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
        
    """
    Set new selectable list to print
    """
    def set(self, list):
        self.list = list

        self.drawList = [ ListElement(unicode(element), self.elementSize) for element in list.getList() ]

        self.update = True
            
        
    """
    handle the event not handled by the gui
    """
    def handle_event(self, event):
        keyActions(event,JOYSTICK_ACTIONS, KEYBOARD_ACTIONS, self.actions)    
                    
    """
    Draw the List object onto the surface
    """
    def draw(self):
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
                       
    """
    Moves the selection up
    """
    def __up(self):
        if len(self.list) != 0:
            self.list.selected = (self.list.selected-1) % len(self.list)
            self.update = True
        
    """
    Moves the selection down
    """
    def __down(self):
        if len(self.list) != 0:
            self.list.selected = (self.list.selected+1) % len(self.list)
            self.update = True
                       
    """
    Returns the (upper) scrollbar position based on the current list position
    """
    def __get_scroll_position(self):
        if self.begin == 0:
            return 0
        else:
            #correct end
            return (((self.height - self.__get_scroll_height()) * self.begin) /
                (len(self.list)  - self.elementsPerPage))
        
    """
    Returns the current scrollbar height based on number of elements.
    """
    def __get_scroll_height(self):
        if len(self.list) <= self.elementsPerPage:
            return self.height
        else:
            return (self.elementsPerPage * self.height) / len(self.list)
        


class ListElement:
    """
    Create a new List Element
    @param caption Text on the new element.
    @param size Size of the new element surface. Tuple of width and height.
    """
    def __init__(self, caption, size):
        self.caption = caption
        self.surface = pygame.Surface(size)
        self.selectedSurface = pygame.Surface(size)
        self.currentSurface = pygame.Surface(size)
        
        self.updateSurface()
      
    """
    Update all list element surfaces.
    """
    def updateSurface(self):
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
    

    """
    Return a surface.
    @return The unselected Surface.
    """
    def getSurface(self):
        return self.surface
    
    """
    Return a surface.
    @return The selected Surface.
    """
    def getSelectedSurface(self):
        return self.selectedSurface

    """
    Return a surface.
    @return The current marked Surface.
    """
    def getCurrentSurface(self):
        return self.currentSurface
