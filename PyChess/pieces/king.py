from piece import Piece


class King(Piece):

    alliance = None

    def __init__(self, alliance):
        self.alliance = alliance
        pass

    def toString(self):
        return "K" if self.alliance == "Black" else "k"