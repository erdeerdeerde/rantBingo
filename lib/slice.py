
import random
import cherrypy
import time
import lib.utils as utils
from time import sleep

import pprint


class Slice():

    def __init__(self, **args):
        player=args.get("player")
        self.name=player.name
        self.Game=args.get("Game")
        self.size=args.get("size", 25)
        self.row_length=5
        self.env=args.get("env")
        self.fields=[]
        self.uri="%s/%s" %(self.Game.name, self.name)
        self.map_fields()
        self.players={player.name: player}
        self.winning_condition=False


    @cherrypy.expose
    def index(self):
        if not utils.auth(self, cherrypy.session):
            raise cherrypy.HTTPRedirect("/login")
        field_template = self.env.get_template('field.j2')
        fields_string = ""
        row_index=0
        for field in self.fields:
            if field.checker == self:
                checked="me"
            elif len(field.checker) > 0:
                checked="enemy"
            else:
                checked="none"

            if row_index == 0:
                fields_string = fields_string + "<tr>"
            fields_string = fields_string + field_template.render(WORD=field.word, WORD_ID=field.word_id, PLAYER=self.name, GAME=self.Game.name, CHECKED=checked)
            if row_index == self.row_length-1:
                fields_string = fields_string + "</tr>\n"
                row_index=0
            else:
                row_index += 1
        tmpl = self.env.get_template('slice.j2')
        return tmpl.render(GAME=self.Game.name, WELCOME_TEXT=self.name, PLAYER=self.name, FIELDS=fields_string)


    @cherrypy.expose
    def update_slice(self):
        #Set the expected headers...
        cherrypy.response.headers["Content-Type"] = "text/event-stream"
        player=cherrypy.session.get('player')
        print "update_slice %s reload %s" %(player.name, player.refresh)
        if self.Game.winner:
            return "event: time\n" + "data: " + "reload" + "winner:" + self.Game.winner.name + "\n\n";
        elif player.refresh:
            player.refresh = False
            i=0
            while player.refresh == False and i <= 6:
                i+=1
                sleep(0.5)
            return "event: time\n" + "data: " + "reload" + "\n\n";
        return "event: time\n" + "data: " + "none" + "\n\n";


    def find_field(self):
        field_found=False
        safety=0
        while not field_found:
            safety +=1
            if safety > 1000:
                raise Exception("not enough words")
            word_id=random.randint(0, len(self.Game.fields)-1)
            field = self.Game.fields[word_id]
            if self in field.owner:
                continue
            # check if word is already used
            if self.Game.check_doublicates and len(field.owner) > 0:
                continue
            field_found=True
        return field


    def map_fields(self):
        while len(self.fields) < self.size:
            field=self.find_field()
            field.owner.append(self)
            self.fields.append(field)
