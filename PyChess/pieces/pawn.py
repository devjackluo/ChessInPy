from piece import Piece


class Pawn(Piece):

    alliance = None

    def __init__(self, alliance):
        self.alliance = alliance
        pass

    def toString(self):
        return "P" if self.alliance == "Black" else "p"