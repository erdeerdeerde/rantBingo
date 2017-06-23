#/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import cherrypy
from cherrypy.lib import sessions
import random
import signal
import string
import json
from jinja2 import Environment, FileSystemLoader
import cPickle as pickle
from lib.game import Game
from lib.player import Player
import lib.utils as utils
import time
import lib.websocket as websocket

import pprint

class Server(object):

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('./templates'))
        self.games={}
        self.players=self.load_players()
        self.wordlists = self.get_wordlist()


    @cherrypy.expose
    def index(self):
        cherrypy.session.debug = True
        login_tmpl = self.env.get_template('login.j2')
        tmpl = self.env.get_template('index.j2')
        initial_wordlist = ""
        game_list = self.games.keys()
        wordlist_ids = self.wordlists.keys()

        if not utils.auth(self, cherrypy.session):
            LOGIN=login_tmpl.render()
        else:
            LOGIN="<h1> Welcome %s</h1>" %cherrypy.session.get('player').name

        return tmpl.render( GAME_LIST = game_list,
                            WORDLIST_IDS = wordlist_ids,
                            INITIAL_WORDLIST = self.wordlists[wordlist_ids[0]],
                            LOGIN = LOGIN)


    @cherrypy.expose
    def login(self, INFO="You are not logged in"):
        stumpf_tmpl=self.env.get_template('stumpf.j2')
        login_tmpl=self.env.get_template('login.j2')
        return stumpf_tmpl.render(CONTENT = login_tmpl.render(INFO = INFO))


    @cherrypy.expose
    def submit(self):
        cherrypy.session.load()

        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)

        pprint.pprint(body)
        print

        #all actions that can be performed without the user being authenticated

        if body["mode"] == "login":
            # $(sanity_check)
            player=body["player"]
            secret=body["secret"]
            if player in self.players.keys() and secret == self.players[player].secret:
                cherrypy.session.__setitem__("player", self.players[player])
                return self.craft_response({"mode": "success", "message": "You are now logged in"})
            else:
                return self.craft_response({"mode": "failure", "message": "Login failed!"})

        elif body["mode"] == "register":
            player=body["player"]
            secret=body["secret"]
            if player in self.players.keys():
                return self.craft_response({"mode": "failure", "message": "Player exists!"})
            else:
                new_player=Player(name=player, secret=secret)
                self.players[player] = new_player
                cherrypy.session.__setitem__("player", self.players[player])
                self.save_players()
                return self.craft_response({"mode": "success", "message": "Player created"})

        elif body["mode"] == "join_as_spectator":
            game_name=body['game_name']
            print "not implemented"
            return self.craft_response({"mode": "failure", "message": "not implemented"})

        elif body["mode"] == "get_wordlist":
            if body['wordlist'] in self.wordlists.keys():
                return self.craft_response({"mode": "success", "return_data": '\n'.join(self.wordlists[body['wordlist']])})

        elif body['mode'] == "get_game_description":
            pprint.pprint(self.games)
            return "foobar"

        #check if the user is authenticated and redirect to /login when he isnt

        if not utils.auth(self, cherrypy.session):
            return self.craft_response({"mode": "redirect", "uri": '/login'})

        #these actions can only be performed when the user is authenticated

        if body["mode"] == "create_game":
            title=body["title"]
            wordlist=body["wordlist"].splitlines()
            game_uri = self.create_game(name=title, wordlist=wordlist)
            if game_uri:
                return self.craft_response({"mode": "success", "message": 'new game created'})
            return self.craft_response({"mode": "failure", "message": "could not create game, does it exist?"})

        elif body["mode"] == "join_game":
            game=body["game"]
            player=cherrypy.session.get('player')
            return self.craft_response({"mode": "redirect", "uri": self.games[game].generate_slice(player=player, env=self.env)})
            #    return self.craft_response({"mode": "redirect", "uri": self.games[game].slices[player.name].uri})
            #uri = self.games[game].slices[player.name].uri
            #self.craft_response({"mode": "redirect", "uri": uri})

        elif body["mode"] == "check_field":
            game=body["game"]
            word_id=int(body["word_id"])
            player=cherrypy.session.get('player')
            self.games[game].fields[word_id].check_field(player)
            return self.craft_response({"mode": "reload"})

        else:
            return 404

        return 503


    def create_game(self, name = "", wordlist=""):
        for game in self.games.keys():
            if self.games[game] == name:
                return False

        wordlist = [i for i in wordlist if i.strip()]

        new_game=Game(name=name, wordlist=wordlist, env=self.env)
        self.games[name]=new_game
        cherrypy.tree.mount(websocket.Ws(), new_game.uri, {
                               '/subscribe' : {
                                 'tools.websocket.on'          : True,
                                 'tools.websocket.handler_cls' : websocket.Subscribe
                               }
                             })
        cherrypy.engine.signals.subscribe()
        return new_game.uri


    def check_player(self, name, secret):
        """checks if a given player name and secret match"""
        if name in self.players.keys() and self.players[name].secret == secret:
            return self.players[name]
        else:
            return False


    def load_players(self, filename='players.plk'):
        """loads the players from file and returns them in a dict"""
        try:
            with open(filename, 'rb') as afile:
                return pickle.load(afile)
        except IOError as e:
            print "IOError: opening '" + filename + "' " + e[1]
        return {}


    def save_players(self, filename='players.plk'):
        """dumps the self.players dict as json into a file"""
        try:
            with open(filename, 'wb') as afile:
                pickle.dump(self.players, afile, pickle.HIGHEST_PROTOCOL)
                return True
        except IOError as e:
            print "IOError: opening '" + filename + "' " + e[1]
            return False


    def craft_response(self, content):
        content = json.dumps(content)
        return content


    def get_wordlist(self):
        """gets the content of all wordlists and returns them in a dict"""
        wordlists = os.listdir('wordlists')
        return_dict = {}
        for f in wordlists:
            with open('wordlists/' + f, 'rb') as afile:
                return_dict[f] = afile.read().decode('utf8').splitlines()
        return return_dict



cherrypy.config.update({'server.socket_port': 9090,
                        'server.socket_host': '0.0.0.0',
                        'autoreload.on': True,
                        'server.show_tracebacks': True,  # disable in production, enable for debugging
                        'tools.sessions.on': True,
                        'tools.sessions.secure': False,   # enable in production, disable for debugging
                        'tools.sessions.timeout': 86400, # set session timeout to 1 day
                        'tools.sessions.httponly': True
                        })

conf_index = {
    '/': {'tools.response_headers.on': True,
          'tools.response_headers.headers': [('Content-Type', 'text/html')],
          'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
    },
    '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
    },
    '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
    }
}

websocket.init_websocket()
cherrypy.tree.mount(Server(), '/', config = conf_index)
cherrypy.engine.start()
cherrypy.engine.block()
