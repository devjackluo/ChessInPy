from tile import Tile
from piece import Piece
from pieces import rook
from pieces import king
from pieces import queen
from pieces import knight
from pieces import bishop
from pieces import pawn
from pieces import nullPiece

class Board:

    gameTiles = {}

    def __init__(self):
        pass

    def createBoard(self):
        for x in range(64):
            self.gameTiles[x] = Tile(x, nullPiece.NullPiece())
        self.gameTiles[0] = Tile(0, rook.Rook("Black"))
        self.gameTiles[1] = Tile(1, knight.Knight("Black"))
        self.gameTiles[2] = Tile(2, bishop.Bishop("Black"))
        self.gameTiles[3] = Tile(3, queen.Queen("Black"))
        self.gameTiles[4] = Tile(4, king.King("Black"))
        self.gameTiles[5] = Tile(5, bishop.Bishop("Black"))
        self.gameTiles[6] = Tile(6, knight.Knight("Black"))
        self.gameTiles[7] = Tile(7, rook.Rook("Black"))
        self.gameTiles[8] = Tile(8, pawn.Pawn("Black"))
        self.gameTiles[9] = Tile(9, pawn.Pawn("Black"))
        self.gameTiles[10] = Tile(10, pawn.Pawn("Black"))
        self.gameTiles[11] = Tile(11, pawn.Pawn("Black"))
        self.gameTiles[12] = Tile(12, pawn.Pawn("Black"))
        self.gameTiles[13] = Tile(13, pawn.Pawn("Black"))
        self.gameTiles[14] = Tile(14, pawn.Pawn("Black"))
        self.gameTiles[15] = Tile(15, pawn.Pawn("Black"))

        self.gameTiles[48] = Tile(48, pawn.Pawn("White"))
        self.gameTiles[49] = Tile(49, pawn.Pawn("White"))
        self.gameTiles[50] = Tile(50, pawn.Pawn("White"))
        self.gameTiles[51] = Tile(51, pawn.Pawn("White"))
        self.gameTiles[52] = Tile(52, pawn.Pawn("White"))
        self.gameTiles[53] = Tile(53, pawn.Pawn("White"))
        self.gameTiles[54] = Tile(54, pawn.Pawn("White"))
        self.gameTiles[55] = Tile(55, pawn.Pawn("White"))
        self.gameTiles[56] = Tile(56, rook.Rook("White"))
        self.gameTiles[57] = Tile(57, knight.Knight("White"))
        self.gameTiles[58] = Tile(58, bishop.Bishop("White"))
        self.gameTiles[59] = Tile(59, queen.Queen("White"))
        self.gameTiles[60] = Tile(60, king.King("White"))
        self.gameTiles[61] = Tile(61, bishop.Bishop("White"))
        self.gameTiles[62] = Tile(62, knight.Knight("White"))
        self.gameTiles[63] = Tile(63, rook.Rook("White"))

    def printBoard(self):
        count = 0
        for tiles in range(len(firstBoard.gameTiles)):
            print('|', end=firstBoard.gameTiles[tiles].pieceOnTile.toString())
            count += 1
            if count == 8:
                print('|', end='\n')
                count = 0


firstBoard = Board()
firstBoard.createBoard()
print(firstBoard.gameTiles)
firstBoard.printBoard()