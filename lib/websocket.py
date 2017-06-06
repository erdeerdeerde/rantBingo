import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket


class Ws:

  @cherrypy.expose
  def subscribe(self):
    pass

class Subscribe(WebSocket):

  def opened(self):
    player=cherrypy.session.get('player')
    player.websocket=self
    print "add websocket to player %s" %player.name

  def closed(self, code, reason=None):
    player=cherrypy.session.get('player')
    player.websocket=None
    print "remove websocket from player %s" %player.name

  def received_message(self, message):
    self.send('you are not supposed to send messages.')

def init_websocket():
  cherrypy.tools.websocket = WebSocketTool()
  WebSocketPlugin(cherrypy.engine).subscribe()
  cherrypy.engine.signals.subscribe()
