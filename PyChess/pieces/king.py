from piece import Piece


class King(Piece):

    alliance = None
    position = None
    possibleMoveVectors = [-9, -7, 7, 9, -8, -1, 1, 8]

    def __init__(self, alliance, position):
        self.alliance = alliance
        self.positon = position

    def toString(self):
        return "K" if self.alliance == "Black" else "k"

    def calculateLegalMoves(self, board):
        legalMoves = []
        for vector in self.possibleMoveVectors:
            destCoord = self.positon + vector

            badMove = self.calculateEdgeCases(self.positon, vector)
            if not badMove:

                if 0 <= destCoord < 64:
                    destTile = board.gameTiles[destCoord]
                    if destTile.pieceOnTile.toString() == "-":
                        print('can move')
                    else:
                        if not destTile.pieceOnTile.alliance == self.alliance:
                            print('can attack')

        return legalMoves


    def calculateEdgeCases(self, position, vector):
        if position in Piece.firstCol:
            if vector == -9 or vector == 7 or vector == -1:
                return True

        if position in Piece.eighthCol:
            if vector == -7 or vector == 9 or vector == 1:
                return True

        return False