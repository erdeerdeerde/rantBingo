
import cherrypy

class Field():
    def __init__(self, **args):
        self.word=args.get("word")
        self.word_id=args.get("word_id")
        self.Game=args.get("Game")
        self.owner = []
        self.checker=[]

    def check_field(self, player):
        self.checker.append(player)
        player.refresh = True
        if self.check_winning_condition() and not self.Game.winner:
            self.Game.winner=player
        self.broadcast_change()

    def broadcast_change(self):
        players=self.Game.players
        for player in players.values():
            print "set refresh for %s" %player.name
            player.refresh=True

    def check_winning_condition(self):
        player=cherrypy.session.get('player')
        Slice=self.Game.slices[player.name]
        size=Slice.size
        row_length=Slice.row_length
        pos=Slice.fields.index(self)
        # check for vertical fails
        check_index=pos

        while check_index - row_length >= 0:
            field=Slice.fields[check_index - row_length]
            if len(field.checker) == 0:
                return False
            if field.checker[0] != player:
                return False
            check_index=check_index - row_length
        check_index=pos
        while check_index + row_length < size:
            field=Slice.fields[check_index + row_length]
            if len(field.checker) == 0:
                return False
            if len(field.checker) > 0 and field.checker[0] != player:
                return False
            check_index=check_index + row_length
        # check for horizontal fails
        check_index=pos
        while check_index - 1 >= 0:
            field=Slice.fields[check_index - 1]
            if len(field.checker) == 0:
                return False
            if len(field.checker) > 0 and field.checker[0] != player:
                return False
            check_index=check_index - 1
        check_index=pos
        while check_index + row_length < size:
            field=Slice.fields[check_index + 1]
            if len(field.checker) == 0:
                return False
            if len(field.checker) > 0 and field.checker[0] != player:
                return False
            check_index=check_index + 1

        self.Game.winner = player
        return True
