'''
Directory list for N64-Emulator
'''

from os import listdir

class DirList():
    def __init__(self, dir):
        self.playing = None
        self.selected = 0

        try:
            self.__list = listdir(dir)
        except OSError:
            self.__list = []

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
