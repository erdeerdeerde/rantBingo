
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
        if self.check_winning_condition(player) and not self.Game.winner:
            self.Game.winner=player
        self.broadcast_change()

    def broadcast_change(self):
        for Slice in self.owner:
            for player in Slice.players.values():
                if player.websocket:
                    print "broadcast refresh to %s" %player.name
                    player.websocket.send("reload")

    def check_winning_condition(self, player):
        Slice=self.Game.slices[player.name]
        size=Slice.size
        row_length=Slice.row_length
        pos=Slice.fields.index(self)
        check_index=pos

        found_cond=False

        #horizontal:
        line=pos/row_length
        start=line*row_length
        end=line*row_length+row_length
        for field in range(start, end):
            if len(Slice.fields[field].checker) > 0 and player == Slice.fields[field].checker[0]:
                found_cond=True
            else:
                found_cond=False
                break

        if found_cond:
            self.Game.winner = player
            return found_cond

        #vertical:
        row=pos%row_length
        start=row
        end=(size-row_length)+row
        for field in range(start, end+1, row_length):
            if len(Slice.fields[field].checker) > 0 and player == Slice.fields[field].checker[0]:
                found_cond=True
            else:
                found_cond=False
                break


        return found_cond
