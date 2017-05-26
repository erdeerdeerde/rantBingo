
class Player():

    def __init__(self, **args):
        self.name=args.get("name")
        self.secret=args.get("secret")
        # holds the slices of a player with to corresponding game as key
        self.slices={}
        self.refresh=False
        self.websocket=None
        self.score=0


    def join_game(self, Game):
        new_slice=Game.generate_slice()
        self.games[Game]=new_slice
