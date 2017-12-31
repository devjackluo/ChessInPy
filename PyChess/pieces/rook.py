from piece import Piece

class Rook(Piece):

    alliance = None
    position = None
    possibleMoveVectors = [-8,-1,1,8]

    def __init__(self, alliance, position):
        self.alliance = alliance
        self.positon = position

    def toString(self):
        return "R" if self.alliance == "Black" else "r"

    def calculateLegalMoves(self, board):
        legalMoves = []
        for vector in self.possibleMoveVectors:
            destCoord = self.positon
            while 0 <= destCoord < 64:
                badMove = self.calculateEdgeCases(destCoord, vector)
                if badMove:
                    break
                else:
                    destCoord += vector
                    if 0 <= destCoord < 64:
                        destTile = board.gameTiles[destCoord]
                        if destTile.pieceOnTile.toString() == "-":
                            print('can move')
                        else:
                            if not destTile.pieceOnTile.alliance == self.alliance:
                                print('can attack')
                            # break regardless of alliance because blocked
                            break

        return legalMoves



    def calculateEdgeCases(self, position, vector):
        if position in Piece.firstCol:
            if vector == -1:
                return True

        if position in Piece.eighthCol:
            if vector == 1:
                return True

        return False