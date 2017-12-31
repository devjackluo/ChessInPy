from piece import Piece

class Bishop(Piece):

    alliance = None

    def __init__(self, alliance):
        self.alliance = alliance
        pass

    def toString(self):
        return "B" if self.alliance == "Black" else "b"