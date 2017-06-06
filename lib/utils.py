import cherrypy
from ws4py.websocket import WebSocket

import pprint

def auth(self, session):

   if ('player' in session.keys()) and (session.get('player').name in self.players.keys()):
       return True
   else:
       return False

