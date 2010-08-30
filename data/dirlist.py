'''
Directory list for N64-Emulator
'''

from os import listdir
import re

from settings.pyemu import *


def romFilter(filename):
    for end in ENDINGS:
        if re.search(end,filename):
            return True
    return False
    

class DirList():
    def __init__(self, dir):
        self.playing = None
        self.selected = 0

        try:
            self.__list = listdir(dir)
        except OSError:
            self.__list = []

        #filter list
        self.__list = filter(romFilter,self.__list)

    def getList(self):
        return self.__list

    def setSelected(self, select):
         if(select > len(self.__list)-1):
            self.selected = len(self.__list)-1
         elif(select < 0):
            self.selected = 0
         else:
            self.selected = select        

    def __len__(self):
        return len(self.__list)
