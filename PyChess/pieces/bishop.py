from pieces.piece import Piece

class Bishop(Piece):

    alliance = None
    position = None
    possibleMoveVectors = [-9, -7, 7, 9]
    value = 300

    def __init__(self, alliance, position):
        self.alliance = alliance
        self.position = position

    def toString(self):
        return "B" if self.alliance == "Black" else "b"


    def calculateLegalMoves(self, board):

        legalMoves = []
        for vector in self.possibleMoveVectors:
            destCoord = self.position
            while 0 <= destCoord < 64:
                badMove = self.calculateEdgeCases(destCoord, vector)
                if badMove:
                    #print('bad')
                    break
                else:
                    destCoord += vector
                    if 0 <= destCoord < 64:
                        destTile = board.gameTiles[destCoord]
                        if destTile.pieceOnTile.toString() == "-":
                            legalMoves.append(destCoord)
                        else:
                            if not destTile.pieceOnTile.alliance == self.alliance:
                                legalMoves.append(destCoord)
                            # break regardless of alliance because blocked
                            break

        return legalMoves


    def calculateEdgeCases(self, position, vector):
        if position in Piece.firstCol:
            if vector == -9 or vector == 7:
                return True

        if position in Piece.eighthCol:
            if vector == -7 or vector == 9:
                return True

        return False