#/usr/bin/env python

import os
import cherrypy
from cherrypy.lib import sessions
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
import pprint


class Ws:

  @cherrypy.expose
  def test(self):
    print "SUBSCRIBE CALLED"
    pass

  @cherrypy.expose
  def index(self):
    return """
<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<body>
    <script>
        var websocket = new WebSocket('ws://127.0.0.1:9090/test');
        websocket.onopen    = function (evt) { console.log("Connected to WebSocket server."); };
        websocket.onclose   = function (evt) { console.log("Disconnected"); };
        websocket.onmessage = function (evt) { event_listener (evt); };
        websocket.onerror   = function (evt) { console.log('Error occured: ' + evt.data); };

        function event_listener (event) {
             console.log(event.data);
         };
        function send_data (data) {
             console.log("sending data:" + data);
             websocket.send(data);
        };
        function close_ws_conn() {
            console.log("Closing socket");
            websocket.close();
        };
    </script>
<p>websocket test</p>
<button id='foo' value='send_data' type='submit' onClick='send_data("test");'>test</button>
<br>
<br>
<button id='bar' value='close' type='submit' onClick='close_ws_conn();'>close</button>
</body>
</html>
"""

class Test(WebSocket):

  def opened(self):
    #pprint.pprint(cherrypy.session)
    #user=cherrypy.session.get('user')
    #user.websocket = self
    #pprint.pprint(user.websocket)
    #pprint.pprint(foobar)
    print "websocket opened"

  def close(self, code, reason=None):
    #pprint.pprint(cherrypy.session)
    #user=cherrypy.session.get('user')
    #pprint.pprint(user)
    pprint.pprint(foobar)
    print "websocket close"

  def received_message(self, message):
    #pprint.pprint(cherrypy.session)
    #sess=cherrypy.session.load()
    #pprint.pprint(foobar)
    pprint.pprint(message)
    print "websocket received message"



cherrypy.config.update({'server.socket_port': 9090,
                        'server.socket_host': '127.0.0.1',
                        'server.show_tracebacks': True,
                        'tools.sessions.on': True,
                        'tools.sessions.secure': False,
                        'tools.sessions.timeout': 60,
                        'tools.sessions.httponly': True
                        })

WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()
cherrypy.tree.mount(Ws(), '/', {
                       '/': {'tools.response_headers.on': True,
                             'tools.response_headers.headers': [
                                    ('X-Frame-options', 'deny'),
                                    ('X-XSS-Protection', '1; mode=block'),
                                    ('X-Content-Type-Options', 'nosniff')],
                             'tools.staticdir.root': os.path.abspath(os.getcwd())
                        },
                       '/test' : {
                         'tools.websocket.on'          : True,
                         'tools.websocket.handler_cls' : Test
                       }
                     })
cherrypy.engine.start()
cherrypy.engine.block()
