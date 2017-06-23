
import random
import cherrypy
import time
import lib.utils as utils
from time import sleep
from urlparse import urlparse

import pprint


class Slice():

    def __init__(self, **args):
        self.player=args.get("player")
        self.name=self.player.name
        self.Game=args.get("Game")
        self.size=args.get("size", 25)
        self.row_length=5
        self.env=args.get("env")
        self.fields=[]
        self.uri="%s/%s" %(self.Game.name, self.name)
        self.map_fields()
        self.players={self.player.name: self.player}
        self.winning_condition=False
        self.score=0


    @cherrypy.expose
    def index(self):
        if not utils.auth(self, cherrypy.session):
            raise cherrypy.HTTPRedirect("/login")
        if self.Game.winner:
            field_template = self.env.get_template('field_disabled.j2')
            WELCOME_TEXT="And the Winner is: %s" %self.Game.winner.name
        else:
            field_template = self.env.get_template('field.j2')
            WELCOME_TEXT=self.name
        fields_string = self.render_fields(field_template)
        if self.Game.winner:
            fields_string = fields_string + self.render_fields(field_template, self.Game.winner)
        tmpl = self.env.get_template('slice.j2')
        url=urlparse(cherrypy.url())
        WEBSOCKET = "%s/%s/subscribe" %(url.netloc, self.Game.name)
        STATS=""
        for Slice in self.Game.slices.values():
            STATS = STATS + "%s: %s" %(Slice.name, Slice.score)
        return tmpl.render(GAME=self.Game.name, WELCOME_TEXT=WELCOME_TEXT, PLAYER=self.name, FIELDS=fields_string, WEBSOCKET=WEBSOCKET, STATS=STATS)

    def find_colour(self, field):
        if len(field.checker) > 0:
            for player in self.players.values():
                if player == field.checker[0]:
                    return "me"
            return "enemy"
        return "none"

    def render_fields(self, field_template, winner=None):
        fields_string = ""
        row_index=0
        if winner:
            fields=self.Game.slices[winner.name]
            player=winner.name
        else:
            fields=self.fields
            player=self.name
        for field in fields:
            checked=self.find_colour(field)
            if row_index == 0:
                fields_string = fields_string + "<tr>"
            fields_string = fields_string + field_template.render(WORD=field.word, WORD_ID=field.word_id, PLAYER=player, GAME=self.Game.name, CHECKED=checked)
            if row_index == self.row_length-1:
                fields_string = fields_string + "</tr>\n"
                row_index=0
            else:
                row_index += 1
        return fields_string

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
