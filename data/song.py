"""
 Song abstract for MPD-Songs
"""

class Song():
    
    def __init__(self, dict):
        self.__songInfo = dict
        
    def __getattr__(self, attr):
        try:
            ret = self.__songInfo[attr]
        except KeyError:
            raise  AttributeError("'%s' object has no attribute '%s'" %
                                    (self.__class__.__name__, attr))
        
        return ret
        
    
    def __unicode__(self):
        try:
            title = self.title
        except AttributeError:
            title = ''
            
        #Title attribute can be a list
        if isinstance(title, list):
            title = title[0]
            
        try:
            artist = self.artist
        except AttributeError:
            artist = ''
            
        return ('%s - %s' % (unicode(artist, 'utf-8'), unicode(title, 'utf-8')))
        
    def __str__(self):
        return unicode()
