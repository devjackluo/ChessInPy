from piece import Piece

class Rook(Piece):

    alliance = None

    def __init__(self, alliance):
        self.alliance = alliance
        pass

    def toString(self):
        return "R" if self.alliance == "Black" else "r"