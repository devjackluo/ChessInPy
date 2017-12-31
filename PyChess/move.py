from tile import Tile
from piece import Piece
from pieces import rook
from pieces import king
from pieces import queen
from pieces import knight
from pieces import bishop
from pieces import pawn
from pieces import nullPiece
from chessBoard import Board


class Move:

    board = None
    movedPiece = None
    destination = None
    gameTiles = {}
    newBoard = None

    def __init__(self, board, movePiece, destination):
        self.board = board
        self.movedPiece = movePiece
        self.destination = destination

    def createNewBoard(self):

        for tile in range(64):
            #print(tile)
            if not tile == self.movedPiece.position and not tile == self.destination:
                self.gameTiles[tile] = self.board.gameTiles[tile]
            else:
                self.gameTiles[tile] = Tile(tile, nullPiece.NullPiece())

        updatePiece = self.movedPiece
        updatePiece.position = self.destination
        self.gameTiles[self.destination] = Tile(self.destination, updatePiece)
        return self.gameTiles







