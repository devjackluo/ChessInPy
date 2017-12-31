from piece import Piece


class Pawn(Piece):

    alliance = None
    position = None
    possibleMoveVectors = [7,9,8,16]
    allianceMultiple = None
    firstMove = True

    def __init__(self, alliance, position):
        self.alliance = alliance
        self.positon = position
        if self.alliance == "Black":
            self.allianceMultiple = 1
        else:
            self.allianceMultiple = -1

    def toString(self):
        return "P" if self.alliance == "Black" else "p"

    def calculateLegalMoves(self, board):

        legalMoves = []
        print(self.possibleMoveVectors)
        print(self.allianceMultiple)

        for vector in self.possibleMoveVectors:

            destCoord = self.positon + (vector*self.allianceMultiple)

            if 0 <= destCoord < 64:

                if vector == 8 and board.gameTiles[destCoord].pieceOnTile.toString() == "-":

                    if self.alliance == "Black" and destCoord in Piece.eighthRow:
                        legalMoves.append(destCoord)
                    elif self.alliance == "White" and destCoord in Piece.firstRow:
                        legalMoves.append(destCoord)
                    else:
                        legalMoves.append(destCoord)

                elif vector == 16 and self.firstMove:

                    behindJump = self.positon + (8 * self.allianceMultiple)
                    if board.gameTiles[behindJump].pieceOnTile.toString() == "-":
                        if board.gameTiles[destCoord].pieceOnTile.toString() == "-":
                            legalMoves.append(destCoord)

                elif vector == 7:

                    if (not self.positon in Piece.eighthCol and not self.alliance == "White") or (not self.positon in Piece.firstCol and not self.alliance == "Black"):

                            if not board.gameTiles[destCoord].pieceOnTile.toString() == "-":
                                piece = board.gameTiles[destCoord].pieceOnTile
                                if not self.alliance == piece.alliance:

                                    if self.alliance == "Black" and destCoord in Piece.eighthRow:
                                        legalMoves.append(destCoord)
                                    elif self.alliance == "White" and destCoord in Piece.firstRow:
                                        legalMoves.append(destCoord)
                                    else:
                                        legalMoves.append(destCoord)

                            elif not board.enPassPawn == None:

                                if board.enPassPawnBehind == destCoord:
                                    enPP = board.enPassPawn
                                    if not self.alliance == enPP.alliance:
                                        legalMoves.append(destCoord)


                elif vector == 9:

                    if (not self.positon in Piece.firstCol and not self.alliance == "White") or (not self.positon in Piece.eighthCol and not self.alliance == "Black"):

                            if not board.gameTiles[destCoord].pieceOnTile.toString() == "-":
                                piece = board.gameTiles[destCoord].pieceOnTile
                                if not self.alliance == piece.alliance:

                                    if self.alliance == "Black" and destCoord in Piece.eighthRow:
                                        legalMoves.append(destCoord)
                                    elif self.alliance == "White" and destCoord in Piece.firstRow:
                                        legalMoves.append(destCoord)
                                    else:
                                        legalMoves.append(destCoord)

                            elif not board.enPassPawn == None:

                                if board.enPassPawnBehind == destCoord:
                                    enPP = board.enPassPawn
                                    if not self.alliance == enPP.alliance:
                                        legalMoves.append(destCoord)


        return legalMoves

