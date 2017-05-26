import cherrypy
from ws4py.websocket import WebSocket

import pprint

def auth(self, session):

   if ('player' in session.keys()) and (session.get('player').name in self.players.keys()):
       return True
   else:
       return False

class Broadcaster(WebSocket):
    def __init__(self, *args, **kw):
        WebSocket.__init__(self, *args, **kw)
        player=cherrypy.session.get('player')
        player.websocket=self
        print "add websocket to player %s" %player.name

    def closed(self, code, reason=None):
        player=cherrypy.session.get('player')
        player.websocket=None
