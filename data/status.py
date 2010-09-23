"""
 Status abstract for MPD-Status
"""

class Status():    
    def __init__(self):
        self.connected = False
        
    def setDisconnected(self):
        self.connected = False

    def update(self, dict):
        self.connected
        
        self.state = dict['state']
        self.volume = dict['volume']
        
        self.playlist = dict['playlist']
        self.playlistlength = dict['playlistlength']
        
        self.repeat = dict['repeat']
        self.consume = dict['consume']
        self.random = dict['random']
        self.xfade = dict['xfade']
        self.single = dict['single']
        
        if self.state == 'play' or self.state == 'pause':
            try:
                self.songid = int(dict['songid'])
                self.song = int(dict['song'])
            
                self.nextsongid = int(dict['nextsongid'])
                self.nextsong = int(dict['nextsong'])
            
                self.time = dict['time']
                self.audio = dict['audio']
                self.bitrate = dict['bitrate']
            except KeyError:
                pass
        else:
            try:
                del self.songid
                del self.song
            
                del self.nextsongid
                del self.nextsong
            
                del self.time
                del self.audio
                del self.bitrate
            except AttributeError:
                pass 
