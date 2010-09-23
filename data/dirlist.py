"""
Directory list for N64-Emulator.
Selectable list for the list GUI element.
"""

from os import listdir
import re

from settings.pyemu import *
from list import List


def romFilter(filename):
    """
    Returns:
        True if filename is a SNES rom image.
    """
    for end in ENDINGS:
        if re.search(end,filename):
            return True
    return False
    

class DirList(List):
    def __init__(self, dir):
        """
        Create a new list from directory. The files a filtered for SNES Images.
        """
        self.playing = None
        self.selected = 0

        try:
            self.list = listdir(dir)
        except OSError:
            self.list = []

        #Filter list.
        self.list = filter(romFilter,self.list)
