"""
MPD data collection and management.
"""

from mpd import (MPDClient, CommandError, ConnectionError, ProtocolError)
import socket

from playlist import Playlist
import status

def remoteAccess(Error):
    """
    Decorator for remote access to mpd server to prevent updates when
    not connected.
    Raises:
        MpdUpdateError: An error occoured while sending a command to
            the connected server.
        MpdNotConnected: The client is not connected to the server while
            trying to send a command.
    """
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
    """
    The MPD-Client is connected but an Error occourd while updating.
    """
    pass


class MpdNotConnected(Exception):
    """
    The MPD-Client is not connected.
    """
    pass

class DataCollector():
    def __init__(self, hostname, port=6600):
        """
        Create a new new connection to MPD-server.
        Args:
            hostname: Hostname of MPD-server.
            port: Port of MPD-Server
        """        
        #Create Status
        self.status = status.Status()
        self.__playlist = None  
        
        #MPD Client setup
        self.__client = MPDClient()
        try:
            self.__connect(hostname,port)
        except socket.error:
            self.connected = False
        else:
            self.connected = True

    def __del__(self):
        """
        Disconnect on destroy.
        """
        try:
            self.__disconnect()
        except ConnectionError:
            pass

    def __connect(self, hostname,port):
        """
        Connect to MPD-server.
        Args:
            hostname: Hostname of MPD-server.
            port: Port of MPD-Server
        """
        self.__client.connect(hostname,port)
        
    @remoteAccess
    def __disconnect(self):
        """
        Disconnect from server.
        """
        self.__client.disconnect()

    @remoteAccess('Getting status not possible')
    def updateStatus(self):
        """
        Update status of MPD-daemon.
        """
        self.status.update(self.__client.status())

    @remoteAccess('Error updating playlist')
    def updatePlaylist(self):
        """
        Updates the playlist from server.
        """
        if self.__playlist:
            selected = self.__playlist.selected
        else:
            selected = 0
        
        self.__playlist = Playlist(self.__client.playlistinfo())
        self.__playlist.setSelected(selected)
        self.__setPlaying()

    def __setPlaying(self):
        """
            Sets the currently playing song in the playlist.
        """
        if self.status.state in ('play','pause'):
            #Correct possible incorrect songid
            for i,song in enumerate(self.__playlist.list):
                if int(song.id) == self.status.songid:
                    self.__playlist.setPlaying(i)
                    break
        else:
            self.__playlist.unsetPlaying()
            

    def getPlaylist(self):
        """
            Returns:
                Playlist data structure.
        """
        return self.__playlist
        
        
    # ##MPD CONTROL##
    
    @remoteAccess('Error during control access.')
    def play(self, songid=-1):
        """
        Start playing the song with songid.
        Args:
            songid: Song ID in the current playlist.
        """
        if songid == -1:
            songid = self.__playlist.selected
        
        #Get songid from playlist because they can differ
        try:
            songid = int(self.__playlist.getSelected().pos)
            print songid
        except IndexError:
            pass
        else:
            self.__client.play(songid)

    @remoteAccess('Error during control access.')
    def pause(self):
        """
        Pause the currently playing song.
        """
        self.__client.pause(1)

    @remoteAccess('Error during control access.')
    def unpause(self):
        """
        Unpause the currently playing song.
        """
        self.__client.pause(0)

    @remoteAccess('Error during control access.')
    def stop(self):
        """
        Stop the currently playing song.
        """
        self.__client.stop()
 
    @remoteAccess('Error during control access.')
    def previous(self):
        """
        Jump to the previous song in the playlist.
        """
        self.__client.previous()

    @remoteAccess('Error during control access.')
    def next(self):
        """
        Jump to the next song in the playlist.
        """
        self.__client.next()

    @remoteAccess('Error during control access.')
    def volume_up(self):
        """
        Raise the music volume 10%.
        """
        if self.status.state == "play":
            volume = int(self.status.volume) + 10
            if volume > 100: volume = 100
            self.__client.setvol(volume)

    @remoteAccess('Error during control access.')
    def volume_down(self):
        """
        Lower the music volume 10%.
        """
        if self.status.state == "play":
            volume = int(self.status.volume) - 10
            if volume < 0 : volume = 0
            self.__client.setvol(volume)

    @remoteAccess('Error during control access.')
    def mute(self):
        """
        Mute the audio output. Sets the volume to 0%.
        """
        if self.status.state == "play":
            self.__client.setvol(0)


    @remoteAccess('Error during control access.')
    def unmute(self):
        """
        Unmute the audio output. Sets the volume to 100%.
        """
        if self.status.state == "play":
            self.__client.setvol(100)

    @remoteAccess('Error removing item from playlist.')
    def delete(self, songid=-1):
        """
        Delete a song from the current playlist.
        Args:
            songid: The song id in the current playlist to be deleted.
        """
        if pos == -1:
            pos = self.__playlist.selected
        try:
            self.__client.delete(pos)
        except CommandError:
            pass

#Testing
if __name__ == '__main__':
    pass