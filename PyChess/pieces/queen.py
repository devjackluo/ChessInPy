from piece import Piece


class Queen(Piece):

    alliance = None

    def __init__(self, alliance):
        self.alliance = alliance
        pass

    def toString(self):
        return "Q" if self.alliance == "Black" else "q"