from piece import Piece


class Knight(Piece):

    alliance = None
    positon = None
    possibleMoveVectors = [-17,-15,-10,-6,6,10,15,17]

    def __init__(self, alliance, position):
        self.alliance = alliance
        self.positon = position


    def toString(self):
        return "N" if self.alliance == "Black" else "n"

    def calculateLegalMoves(self, board):
        legalMoves = []
        for vector in self.possibleMoveVectors:
            destCoord = self.positon + vector
            if 0 <= destCoord < 64:
                badMove = self.calculateEdgeCases(self.positon, vector)
                if not badMove:
                    destTile = board.gameTiles[destCoord]
                    if destTile.pieceOnTile.toString() == "-":
                        legalMoves.append(destCoord)
                    else:
                        if not destTile.pieceOnTile.alliance == self.alliance:
                            legalMoves.append(destCoord)

        return legalMoves


    def calculateEdgeCases(self, position, vector):
        if position in Piece.firstCol:
            if vector == -17 or vector == -10 or vector == 6 or vector == 15:
                return True

        if position in Piece.secondCol:
            if vector == -10 or vector == 6:
                return True

        if position in Piece.seventhCol:
            if vector == -6 or vector == 10:
                return True

        if position in Piece.eighthCol:
            if vector == -15 or vector == -6 or vector == 10 or vector == 17:
                return True

        return False
