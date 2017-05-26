a game for the general merriment.

game concept:
the game takes place in your browser. from the main page you can generate a new game by pasting a wordlist.
the new game will get a unique uri. players can join the game by navigating their browser to this uri and click on "participate".
each player will now get a sub-uri from the game. on this sub-uri there will be a table known from the classical bingo game. per default it will have 5x5 fields.
the fields will have events written in them (e.g. "$(respected co-employee) said $SOMETHING", "$(respected co-employee) did $SOMETHING"). when a predicted event happens the player is ought to click the respective field.


tecnical concept
the page itself is nothing more than a html table with links in it. all the logic takes place in python code. the webserver is realized by cherrypy.
the code is split into the following classes:
 - main  -> glues everything together
 - game  -> holds the wordlist, the uri, the player sub-uri
 - slice -> holds the 5x5 (default) array with fields
 - field -> holds one line of the wordlist, a unique uri which is called when the field is clicked on


ToDo:
 - hardening of the code so it can be hosted on the internets
 - scoring: difficult words or sentences give more points
 - highscore: players retain the points collected in a game
