from tile import Tile
from pieces import rook
from pieces import king
from pieces import queen
from pieces import knight
from pieces import bishop
from pieces import pawn
from pieces import nullPiece

class Board:

    gameTiles = {}
    enPassPawn = None
    enPassPawnBehind = None
    currentPlayer = "White"

    def __init__(self):
        pass

    def calculateActivePieces(self, alliance):

        activeP = []
        for tile in range(len(self.gameTiles)):
            if not self.gameTiles[tile].pieceOnTile.toString() == "-":
                if self.gameTiles[tile].pieceOnTile.alliance == alliance:
                    activeP.append(self.gameTiles[tile].pieceOnTile)

        return activeP

    def calculateLegalMoves(self, pieces, board):
        allLegals = []
        for piece in pieces:
            pieceMoves = piece.calculateLegalMoves(board)
            for move in pieceMoves:
                allLegals.append([move, piece])
        return allLegals


    def createBoard(self):

        for x in range(64):
            self.gameTiles[x] = Tile(x, nullPiece.NullPiece())
        self.gameTiles[0] = Tile(0, rook.Rook("Black", 0))
        self.gameTiles[1] = Tile(1, knight.Knight("Black", 1))
        self.gameTiles[2] = Tile(2, bishop.Bishop("Black", 2))
        self.gameTiles[3] = Tile(3, queen.Queen("Black", 3))
        self.gameTiles[4] = Tile(4, king.King("Black", 4))
        self.gameTiles[5] = Tile(5, bishop.Bishop("Black", 5))
        self.gameTiles[6] = Tile(6, knight.Knight("Black", 6))
        self.gameTiles[7] = Tile(7, rook.Rook("Black", 7))
        self.gameTiles[8] = Tile(8, pawn.Pawn("Black", 8))
        self.gameTiles[9] = Tile(9, pawn.Pawn("Black", 9))
        self.gameTiles[10] = Tile(10, pawn.Pawn("Black", 10))
        self.gameTiles[11] = Tile(11, pawn.Pawn("Black", 11))
        self.gameTiles[12] = Tile(12, pawn.Pawn("Black", 12))
        self.gameTiles[13] = Tile(13, pawn.Pawn("Black", 13))
        self.gameTiles[14] = Tile(14, pawn.Pawn("Black", 14))
        self.gameTiles[15] = Tile(15, pawn.Pawn("Black", 15))

        # self.gameTiles[25] = Tile(25, pawn.Pawn("White", 25))
        # #self.gameTiles[18] = Tile(18, pawn.Pawn("Black", 18))
        # self.gameTiles[26] = Tile(26, pawn.Pawn("Black", 26))
        # self.gameTiles[24] = Tile(24, pawn.Pawn("Black", 24))

        self.gameTiles[48] = Tile(48, pawn.Pawn("White", 48))
        self.gameTiles[49] = Tile(49, pawn.Pawn("White", 49))
        self.gameTiles[50] = Tile(50, pawn.Pawn("White", 50))
        self.gameTiles[51] = Tile(51, pawn.Pawn("White", 51))
        self.gameTiles[52] = Tile(52, pawn.Pawn("White", 52))
        self.gameTiles[53] = Tile(53, pawn.Pawn("White", 53))
        self.gameTiles[54] = Tile(54, pawn.Pawn("White", 54))
        self.gameTiles[55] = Tile(55, pawn.Pawn("White", 55))
        self.gameTiles[56] = Tile(56, rook.Rook("White", 56))
        self.gameTiles[57] = Tile(57, knight.Knight("White", 57))
        self.gameTiles[58] = Tile(58, bishop.Bishop("White", 58))
        self.gameTiles[59] = Tile(59, queen.Queen("White", 59))
        self.gameTiles[60] = Tile(60, king.King("White", 60))
        self.gameTiles[61] = Tile(61, bishop.Bishop("White", 61))
        self.gameTiles[62] = Tile(62, knight.Knight("White", 62))
        self.gameTiles[63] = Tile(63, rook.Rook("White", 63))

    def printBoard(self):
        count = 0
        for tiles in range(len(self.gameTiles)):
            print('|', end=self.gameTiles[tiles].pieceOnTile.toString())
            count += 1
            if count == 8:
                print('|', end='\n')
                count = 0




# firstBoard = Board()
# firstBoard.createBoard()
# print(firstBoard.gameTiles)
# firstBoard.printBoard()
#firstBoard.gameTiles[1].pieceOnTile.calculateLegalMoves(firstBoard)
#firstBoard.gameTiles[0].pieceOnTile.calculateLegalMoves(firstBoard)
#firstBoard.gameTiles[2].pieceOnTile.calculateLegalMoves(firstBoard)
#firstBoard.gameTiles[3].pieceOnTile.calculateLegalMoves(firstBoard)
#firstBoard.gameTiles[4].pieceOnTile.calculateLegalMoves(firstBoard)
#firstBoard.gameTiles[9].pieceOnTile.calculateLegalMoves(firstBoard)
#firstBoard.gameTiles[55].pieceOnTile.calculateLegalMoves(firstBoard)
# firstBoard.enPassPawn = firstBoard.gameTiles[24].pieceOnTile
# firstBoard.enPassPawnBehind = 16
# firstBoard.gameTiles[25].pieceOnTile.calculateLegalMoves(firstBoard)