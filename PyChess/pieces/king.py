from pieces.piece import Piece


class King(Piece):

    alliance = None
    position = None
    possibleMoveVectors = [-9, -7, 7, 9, -8, -1, 1, 8]
    value = 1100

    def __init__(self, alliance, position):
        self.alliance = alliance
        self.position = position

    def toString(self):
        return "K" if self.alliance == "Black" else "k"

    def calculateLegalMoves(self, board):

        legalMoves = []
        for vector in self.possibleMoveVectors:
            destCoord = self.position + vector

            badMove = self.calculateEdgeCases(self.position, vector)
            if not badMove:

                if 0 <= destCoord < 64:
                    destTile = board.gameTiles[destCoord]
                    if destTile.pieceOnTile.toString() == "-":
                        legalMoves.append(destCoord)
                    else:
                        if not destTile.pieceOnTile.alliance == self.alliance:
                            legalMoves.append(destCoord)


        allEnemyAttacks = []
        enemyPieces = None


        if self.alliance == "Black":

            # for tile in range(64):
            #     if not board.gameTiles[tile].pieceOnTile.toString() == "-":
            #         if not board.gameTiles[tile].pieceOnTile.alliance == self.alliance:
            #             enemyPieces.append(board.gameTiles[tile].pieceOnTile)
            enemyPieces = board.calculateActivePieces("White")

            for enemy in range(len(enemyPieces)):
                if not enemyPieces[enemy].toString() == "k":
                    moves = enemyPieces[enemy].calculateLegalMoves(board)
                else:
                    moves = enemyPieces[enemy].helperCalLegalMoves(board)
                for move in range(len(moves)):
                    allEnemyAttacks.append(moves[move])

        elif self.alliance == "White":

            # for tile in range(64):
            #     if not board.gameTiles[tile].pieceOnTile.toString() == "-":
            #         if not board.gameTiles[tile].pieceOnTile.alliance == self.alliance:
            #             enemyPieces.append(board.gameTiles[tile].pieceOnTile)
            enemyPieces = board.calculateActivePieces("Black")

            for enemy in range(len(enemyPieces)):
                if not enemyPieces[enemy].toString() == "K":
                    moves = enemyPieces[enemy].calculateLegalMoves(board)
                else:
                    moves = enemyPieces[enemy].helperCalLegalMoves(board)
                for move in range(len(moves)):
                    allEnemyAttacks.append(moves[move])


        if self.firstMove and self.alliance == "Black":

            if board.gameTiles[0].pieceOnTile.toString() == "R" and board.gameTiles[2].pieceOnTile.firstMove:
                if board.gameTiles[1].pieceOnTile.toString() == "-":
                    if board.gameTiles[2].pieceOnTile.toString() == "-":
                        if board.gameTiles[3].pieceOnTile.toString() == "-":
                            if not 3 in allEnemyAttacks and not 2 in allEnemyAttacks and not 4 in allEnemyAttacks:
                                legalMoves.append(2)

            if board.gameTiles[7].pieceOnTile.toString() == "R" and board.gameTiles[2].pieceOnTile.firstMove:
                if board.gameTiles[6].pieceOnTile.toString() == "-":
                    if board.gameTiles[5].pieceOnTile.toString() == "-":
                        if not 5 in allEnemyAttacks and not 6 in allEnemyAttacks and not 4 in allEnemyAttacks:
                            legalMoves.append(6)

        elif self.firstMove and self.alliance == "White":

            if board.gameTiles[56].pieceOnTile.toString() == "r" and board.gameTiles[2].pieceOnTile.firstMove:
                if board.gameTiles[57].pieceOnTile.toString() == "-":
                    if board.gameTiles[58].pieceOnTile.toString() == "-":
                        if board.gameTiles[59].pieceOnTile.toString() == "-":
                            if not 58 in allEnemyAttacks and not 59 in allEnemyAttacks and not 60 in allEnemyAttacks:
                                legalMoves.append(58)

            if board.gameTiles[63].pieceOnTile.toString() == "r" and board.gameTiles[2].pieceOnTile.firstMove:
                if board.gameTiles[62].pieceOnTile.toString() == "-":
                    if board.gameTiles[61].pieceOnTile.toString() == "-":
                        if not 62 in allEnemyAttacks and not 61 in allEnemyAttacks and not 60 in allEnemyAttacks:
                            legalMoves.append(62)

        finalLegal = []
        for move in legalMoves:
            if not move in allEnemyAttacks:
                finalLegal.append(move)

        return finalLegal


    def calculateEdgeCases(self, position, vector):
        if position in Piece.firstCol:
            if vector == -9 or vector == 7 or vector == -1:
                return True
        if position in Piece.eighthCol:
            if vector == -7 or vector == 9 or vector == 1:
                return True
        return False


    def helperCalLegalMoves(self, board):

        legalMoves = []
        for vector in self.possibleMoveVectors:
            destCoord = self.position + vector
            badMove = self.calculateEdgeCases(self.position, vector)
            if not badMove:
                if 0 <= destCoord < 64:
                    destTile = board.gameTiles[destCoord]
                    if destTile.pieceOnTile.toString() == "-":
                        legalMoves.append(destCoord)
                    else:
                        if not destTile.pieceOnTile.alliance == self.alliance:
                            legalMoves.append(destCoord)

        return legalMoves

