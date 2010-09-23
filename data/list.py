"""
Selectable list abstract for the use with the list gui element.
"""


class List():
    def init(self):
        self.list = []
    
    def getList(self):
        """
        Returns:
            The current filtered file list.
        """
        return self.list

    def setSelected(self, select):
        """
        Set the currently selected Element in the list.
        """
        if(select > len(self.list)-1):
            self.selected = len(self.list)-1
        elif(select < 0):
            self.selected = 0
        else:
            self.selected = select
 
    def __len__(self):
        """
        Returns:
            The number of unique filenames in the list.
        """
        return len(self.list)