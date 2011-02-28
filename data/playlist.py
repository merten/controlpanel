'''
 Playlist for MPD-Playlists
'''

from song import Song
from list import List

class Playlist(List):

    def __init__(self, list):
        self.selected = 0
        self.playing = None

        self.update(list)
        
    def setPlaying(self, pos):
        """
        Mark the currently playing song in the list.
        Args
            songid: The song to mark as playing.
        """
        self.playing = pos

    def unsetPlaying(self):
        """
        Unset the currently playing marker in the list.
        """
        self.playing = None
        
    def getSelected(self):
        """
        Returns:
            Selected song, None if an error occoured.
        """
        try:
            return self.list[self.selected]
        except IndexError:
            return None
    
    def update(self, list):
        """
        Update the list from a songlist returned by the MPD-server.
        Args:
            list: Playlist as returned by the MPD-server.
        """
        self.list = []

        for songinfo in list:
            self.list.append(Song(songinfo))
