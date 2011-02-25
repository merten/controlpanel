"""
The data class acts as a central class for holding the local data.
This is a copy of the information on the MPD Server.
"""

from threading import Lock

import status

class Data(object):
    def __init__(self):
        self.playlist = None
        self.status = status.Status()
        
        self.__lock = Lock()
    
    def __getattribute__(self,name):
        with super(Data,self).__getattribute__('_Data__lock'):
            return super(Data,self).__getattribute__(name)

