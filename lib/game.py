from lib.slice import Slice
from lib.field import Field
import cherrypy
from lib.utils import Broadcaster

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
cherrypy.tools.websocket = WebSocketTool()
WebSocketPlugin(cherrypy.engine).subscribe()

class Game():
    def __init__(self, **args):
        self.name=args.get("name")
        self.env=args.get("env")
        self.wordlist=args.get("wordlist")
        self.check_doublicates=False
        self.check_checker=False
        self.fields=[]
        self.slices={}
        self.uri="/%s" %self.name
        self.subscribe_conf={"subscribe": {'tools.websocket.on': True,
                                           'tools.websocket.handler_cls': Broadcaster}}
        cherrypy.tree.mount(self, self.uri, config = self.subscribe_conf)
        self.generate_fields()
        self.players={}
        self.winner=None

    @cherrypy.expose
    def subscribe(self):
        print "subscribe"

    def generate_slice(self, player, env):
        for s in self.slices.values():
            if s.name == player.name:
                return s.uri
        new_slice=Slice(player=player, Game=self, env=env)
        self.players[player.name] = player
        cherrypy.tree.mount(new_slice, "/%s/%s" %(self.name,player.name))
        self.slices[player.name] = new_slice
        return new_slice.uri

    def generate_fields(self):
        x=0
        while x < len(self.wordlist):
            word=self.wordlist[x].replace("\"", "&quot;").replace("\'", "&#39;")
            field=Field(word=word, word_id=x, Game=self)
            self.fields.append(field)
            x+=1

    def check_checker(self, word_id, player):
        if not self.check_checker:
            return
        field = self.fields[word_id]
        if len(field.checker) <= 0:
            field.checker.append(player)
        return
