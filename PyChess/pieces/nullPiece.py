from pieces.piece import Piece

class NullPiece(Piece):

    def __init__(self):
        pass

    def toString(self):
        return "-"