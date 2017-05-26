import cherrypy

import pprint

def auth(self, session):

   if ('player' in session.keys()) and (session.get('player').name in self.players.keys()):
       return True
   else:
       return False
