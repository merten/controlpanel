"""
Implements the thread for all access operations to the mpd server.
The communication is done via the event class.
"""

from threading import (Thread, Event)
from Queue import (Empty, Queue)
from mpd import (MPDClient, CommandError, ConnectionError, ProtocolError)
import socket

from playlist import Playlist

class Commander(object):
    def __init__(self):
        self.event = Event()
        
        self.__queue = Queue()

    def __getattr__(self, name):
        def put_command(*args):
            self.put(name, *args)

        return put_command
        
    def put(self, command, *args):
        """
        Put a new command into the command queue.
        """
        self.__queue.put((command, args))
        self.event.set()
        
    def pop(self):
        """
        Get the next command from the queue.
        Returns:
            Dictionary of command, None if empty.
        """
        try:
            cmd = self.__queue.get(block=False)
        except Empty:
            self.event.clear()
            cmd = None
        
        return cmd
    
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
                    return fun(*args)
                except (ConnectionError, CommandError, ProtocolError):
                    raise MpdError(Error)
            else:
                raise MpdNotConnected('Not connected to Host')
        return mpdRemoteAccess
    return decorator

class MpdError(Exception):
    """
    The MPD-Client is connected but an Error occourd while updating.
    """
    pass


class MpdNotConnected(Exception):
    """
    The MPD-Client is not connected.
    """
    pass
    
class Communicator(object):
    """
    Communicates with the MPD server.
    """
    def __init__(self, hostname, port=6600):
        """
        Create a new new connection to MPD-server.
        Args:
            hostname: Hostname of MPD-server.
            port: Port of MPD-Server
        """
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
    def get_status(self):
        """
        Returns status of MPD-daemon.
        """
        return self.__client.status()

    @remoteAccess('Error updating playlist')
    def get_playlist(self):
        """
        Returns the playlist from server.
        """
        return self.__client.playlistinfo()
        
    ###MPD CONTROL###
    @remoteAccess('Error during control access.')
    def play(self, songid):
        """
        Start playing the song with songid.
        Args:
            songid: Song ID in the current playlist.
        """
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
    def set_volume(self, volume):
        """
        Raise the music volume 10%.
        """
        self.__client.setvol(volume)

    @remoteAccess('Error removing item from playlist.')
    def delete(self, songid):
        """
        Delete a song from the current playlist.
        Args:
            songid: The song id in the current playlist to be deleted.
        """
        try:
            self.__client.delete(songid)
        except CommandError:
            #TODO Error handling and Logging
            print "delete CommandError"

class CommanderThread(Thread):
    """
    Does the communication and updates the status.
    """
    def __init__(self,commander, data, hostname='localhost',port=6600):
        Thread.__init__(self)
        
        self.__hostname = hostname
        self.__port = port
        
        self.__commander = commander
        self.__data = data
        self.__communicator = Communicator(hostname,port)
        
        self.__cmd_index = {
                'update_playlist' : self.__update_playlist,
                'update_status' : self.__update_status,
                'play' : self.__play,
                'pause' : self.__pause,
                'unpause' : self.__unpause,
                'stop' : self.__stop,
                'previous' : self.__previous,
                'next' : self.__next,
                'volume_up' : self.__volume_up,
                'volume_down' : self.__volume_down,
                'mute' : self.__mute,
                'unmute' : self.__unmute,
                'delete' : self.__delete}
        
    def run(self):
        while True:
            self.__commander.event.wait()
            cmd = self.__commander.pop()
            
            if cmd == None:
                continue
            
            cmd_method, cmd_args = cmd
            print cmd
            
            try:
                try:
                    if cmd_method in self.__cmd_index:
                        self.__cmd_index[cmd_method](*cmd_args)
                except MpdError:
                    #TODO Logging
                    print "MpdError"
            except MpdNotConnected:
                self.__reconnect()
            
            if cmd_method == 'exit':
                while self.__commander.pop():
                    pass
                del self.__communicator #shut down connection
                break #shut down thread
            
    def __reconnect(self):
        """
        Create a new connection to the MPD server all old connections
        will be closed.
        """
        self.__communicator = Communicator(self.__hostname,self.__port)
            
    def __update_playlist(self):
        """
        Updates the playlist from server.
        """
        self.__data.playlist.update(self.__communicator.get_playlist())
        self.__set_playing()
        
    def __update_status(self):
        """
        Update status of MPD-daemon.
        """
        self.__data.status.update(self.__communicator.get_status())
        
    #TODO move to Data
    def __set_playing(self):
        """
            Sets the currently playing song in the playlist.
        """
        try:
            if self.__data.status.state in ('play','pause'):
                #Correct possible incorrect songid
                for i,song in enumerate(self.__data.playlist.list):
                    if int(song.id) == self.__data.status.songid:
                        self.__data.playlist.setPlaying(i)
                        break
            else:
                self.__data.playlist.unsetPlaying()
        except AttributeError:
            self.__data.playlist.unsetPlaying() 
        
    ###MPD CONTROL###
    def __play(self, songid=-1):
        """
        Start playing the song with songid.
        Args:
            songid: Song ID in the current playlist.
        """
        if self.__data.playlist == None:
            return
        
        if songid == -1:
            songid = self.__data.playlist.selected
        
        #Get songid from playlist because they can differ
        try:
            songid = int(self.__data.playlist.getSelected().pos)
        except IndexError:
            #TODO Error handling
            print "__play Index Error"
        else:
            self.__communicator.play(songid)

    def __pause(self):
        """
        Pause the currently playing song.
        """
        self.__communicator.pause()

    def __unpause(self):
        """
        Unpause the currently playing song.
        """
        self.__communicator.unpause()

    def __stop(self):
        """
        Stop the currently playing song.
        """
        self.__communicator.stop()
 
    def __previous(self):
        """
        Jump to the previous song in the playlist.
        """
        self.__communicator.previous()

    def __next(self):
        """
        Jump to the next song in the playlist.
        """
        self.__communicator.next()

    def __volume_up(self):
        """
        Raise the music volume 10%.
        """
        if self.__data.status.state == "play":
            volume = int(self.__data.status.volume) + 10
            if volume > 100: volume = 100
            self.__communicator.set_volume(volume)

    def __volume_down(self):
        """
        Lower the music volume 10%.
        """
        if self.__data.status.state == "play":
            volume = int(self.__data.status.volume) - 10
            if volume < 0 : volume = 0
            self.__communicator.set_volume(volume)

    def __mute(self):
        """
        Mute the audio output. Sets the volume to 0%.
        """
        if self.__data.status.state == "play":
            self.__data.status.last_volume = int(self.__data.status.volume)
            self.__communicator.set_volume(0)

    def __unmute(self):
        """
        Unmute the audio output. Sets the volume to 100%.
        """
        if self.__data.status.state == "play":
            try:
                self.__communicator.set_volume(self.__data.status.last_volume)
            except AttributeError:
                #TODO Logging
                print "__unmute AttributeError"
            else:
                self.__communicator.set_volume(50)

    def __delete(self, songid=-1):
        """
        Delete a song from the current playlist.
        Args:
            songid: The song id in the current playlist to be deleted.
        """
        if songid == -1:
            songid = self.__data.playlist.selected
            self.__communicator.delete(songid)

