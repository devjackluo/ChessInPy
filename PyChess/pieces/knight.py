from piece import Piece


class Knight(Piece):

    alliance = None

    def __init__(self, alliance):
        self.alliance = alliance
        pass

    def toString(self):
        return "N" if self.alliance == "Black" else "n"