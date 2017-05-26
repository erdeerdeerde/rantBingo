# -*- coding: utf-8 -*-

import cherrypy

import random
import string
import json

#this file can be removed in the future

class Server(object):

#    def index(self):
#        return """<html></html>"""

    @cherrypy.expose
    def index(self):
        return """
<html>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script type='text/javascript'>
function Update() {
    content = $('#title').val();
    content = jQuery.parseJSON(content);
    $.ajax({
      type: 'POST',
      url: "submit",
      contentType: "application/json",
      processData: true,
      data: content,
      success: function(data) {alert(data);},
      dataType: "json"
    });
}
</script>
<body>
<input type='textbox' id='title' value='title' size='20' />
<br>
<input type='textbox' id='wordlist' value='' size='20' />
<br>
<input type='submit' value='Update' onClick='Update(); return false' />
</body>
</html>
"""

    @cherrypy.expose
    def submit(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        #body = json.loads(rawbody)
        print rawbody
        return rawbody

    def run(self):
        cherrypy.config.update({'server.socket_port': 9090})
        conf_index = {
            '/': {
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'text/html')],
            }
        }
#        cherrypy.tree.mount(self, '/', config = conf_index)
#        cherrypy.engine.start()
#        cherrypy.engine.block()
        cherrypy.quickstart(self, '/', conf_index)
