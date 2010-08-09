'''
MPD data collection and management.
'''

from mpd import (MPDClient, CommandError, ConnectionError, ProtocolError)
import socket

from playlist import Playlist
import status

def remoteAccess(Error):
    def decorator(fun):
        def mpdRemoteAccess(*args):
            if args[0].connected:
                try:
                    fun(*args)
                except ConnectionError, ProtocolError:
                    raise MpdUpdateError(Error)
            else:
                raise MpdNotConnected('Not connected to Host')
        return mpdRemoteAccess
    return decorator

class MpdUpdateError(Exception):
    pass


class MpdNotConnected(Exception):
    pass

class DataCollector():
    '''
    Init connection to mpd daemon and set up status
    '''
    def __init__(self, hostname, port=6600):
        """Create Status"""
        self.status = status.Status()
        self.__playlist = None  
        
        """MPD Client"""
        self.__client = MPDClient()
        try:
            self.__connect(hostname,port)
        except socket.error:
            self.connected = False
        else:
            self.connected = True

    '''
    Disconnect on destroy.
    '''
    def __del__(self):
        try:
            self.__disconnect()
        except ConnectionError:
            pass

    '''
    Connect to Server
    '''
    def __connect(self, hostname,port):
        self.__client.connect(hostname,port)
        
    '''
    Disconnect from Server
    '''
    @remoteAccess
    def __disconnect(self):
        self.__client.disconnect()

    '''
    Update status
    '''
    @remoteAccess('Getting status not possible')
    def updateStatus(self):
        self.status.update(self.__client.status())

    '''
    updates the playlist from server
    '''
    @remoteAccess('Error updating playlist')
    def updatePlaylist(self):
        if self.__playlist:
            selected = self.__playlist.selected
        else:
            selected = 0
        self.__playlist = Playlist(self.__client.playlistinfo())
        self.__playlist.setSelected(selected)
        self.__setPlaying()


    def __setPlaying(self):
        if self.status.state in ('play','pause'):
            self.__playlist.setPlaying(self.status.songid)
        else:
            self.__playlist.unsetPlaying()
            

    def getPlaylist(self):
        return self.__playlist

    ''' Controls '''
    
    @remoteAccess('Error during control access.')
    def play(self, pos=-1):
        if pos == -1:
            pos = self.__playlist.selected
        self.__client.play(pos)

    @remoteAccess('Error during control access.')
    def pause(self):
        self.__client.pause(1)

    @remoteAccess('Error during control access.')
    def unpause(self):
        self.__client.pause(0)

    @remoteAccess('Error during control access.')
    def stop(self):
        self.__client.stop()
 
    @remoteAccess('Error during control access.')
    def previous(self):
        self.__client.previous()

    @remoteAccess('Error during control access.')
    def next(self):
        self.__client.next()

    @remoteAccess('Error during control access.')
    def setVol(self, vol=50):
        self.__client.setvol(vol)

    @remoteAccess('Error removing item from playlist.')
    def delete(self, pos=-1):
        if pos == -1:
            pos = self.__playlist.selected
        try:
            self.__client.delete(pos)
        except CommandError:
            pass

''' Testing '''
if __name__ == '__main__':
    dc = DataCollector('localhost',6600)
    
    dc.play()
    dc.updateStatus()
    print dc.status.state
    dc.stop()
    dc.updateStatus()
    print dc.status.state
    
