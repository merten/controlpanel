'''
 Playlist abstract for MPD-Playlists
'''

from song import Song

class Playlist():

    def __init__(self, list):
        self.selected = 0
        self.playing = None

        self.updatePlaylist(list)
        
    def setPlaying(self, pos):
        self.playing = pos

    def unsetPlaying(self):
        self.playing = None

    def getList(self):
        return self.__songs

    
    def updatePlaylist(self, list):
        self.__songs = []

        for songinfo in list:
            self.__songs.append(Song(songinfo))

        self.setSelected(self.selected)

    def setSelected(self, select):
        if(select > len(self.__songs)-1):
            self.selected = len(self.__songs)-1
        elif(select < 0):
            self.selected = 0
        else:
            self.selected = select

    def __len__(self):
        return len(self.__songs)
