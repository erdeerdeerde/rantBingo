
import cherrypy

class Field():
    def __init__(self, **args):
        self.word=args.get("word")
        self.word_id=args.get("word_id")
        self.Game=args.get("Game")
        self.owner = []
        self.checker=[]

    def check_field(self, player):
        if not player in self.checker:
            self.checker.append(player)
            self.word = self.word + "\n" + player.name
        else:
            return
        self.add_points(player)
        if self.check_winning_condition(player) and not self.Game.winner:
            self.Game.winner=player
            self.broadcast_change(everyone=True)
        else:
            self.broadcast_change()

    def add_points(self, player):
        position=self.checker.index(player)
        Slice=self.Game.slices[player]
        Slice.score += 5-position

    def broadcast_change(self, everyone=False):
        if everyone:
            for player in self.Game.players.values():
                print "broadcast refresh to %s" %player.name
                player.websocket.send("reload")
        else:
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
