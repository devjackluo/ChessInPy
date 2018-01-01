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
import copy


class Move:

    board = None
    movedPiece = None
    destination = None



    def __init__(self, board, movePiece, destination):
        self.board = board
        self.movedPiece = movePiece
        self.destination = destination

    def createNewBoard(self):

        newBoard = Board()
        gameTiles = {}





        # TODO CHECK if enpassant attack
        enpassLocation = None
        if self.movedPiece.toString() == 'P':
            if not self.board.enPassPawn == None:
                if self.destination == self.board.enPassPawnBehind:
                    print("b enpassatk")
                    enpassLocation = self.board.enPassPawn.position
        elif self.movedPiece.toString() == 'p':
            if not self.board.enPassPawn == None:
                if self.destination == self.board.enPassPawnBehind:
                    print("w enpassatk")
                    enpassLocation = self.board.enPassPawn.position


        for tile in range(64):
            #print(tile)

            if not tile == self.movedPiece.position and not tile == self.destination and not tile == enpassLocation:
                gameTiles[tile] = self.board.gameTiles[tile]
            else:
                gameTiles[tile] = Tile(tile, nullPiece.NullPiece())



        # TODO Check if it is castle move
        if self.movedPiece.toString() == 'K' and self.movedPiece.firstMove:
            if self.destination == 2:
                if self.board.gameTiles[0].pieceOnTile.toString() == "R" and self.board.gameTiles[0].pieceOnTile.firstMove:
                    print('b qc')
                    gameTiles[0] = Tile(0, nullPiece.NullPiece())
                    gameTiles[3] = Tile(3, rook.Rook("Black", 3))
            elif self.destination == 6:
                if self.board.gameTiles[7].pieceOnTile.toString() == "R" and self.board.gameTiles[7].pieceOnTile.firstMove:
                    print('b kc')
                    gameTiles[7] = Tile(7, nullPiece.NullPiece())
                    gameTiles[5] = Tile(5, rook.Rook("Black", 5))


        elif self.movedPiece.toString() == 'k':
            if self.destination == 58:
                if self.board.gameTiles[56].pieceOnTile.toString() == "r" and self.board.gameTiles[56].pieceOnTile.firstMove:
                    print('w qc')
                    gameTiles[56] = Tile(56, nullPiece.NullPiece())
                    gameTiles[59] = Tile(59, rook.Rook("White", 59))
            elif self.destination == 62:
                if self.board.gameTiles[63].pieceOnTile.toString() == "r" and self.board.gameTiles[56].pieceOnTile.firstMove:
                    print('w kc')
                    gameTiles[63] = Tile(63, nullPiece.NullPiece())
                    gameTiles[61] = Tile(61, rook.Rook("White", 61))



        updatePiece = copy.copy(self.movedPiece)
        updatePiece.firstMove = False
        updatePiece.position = self.destination
        gameTiles[self.destination] = Tile(self.destination, updatePiece)
        newBoard.gameTiles = gameTiles



        # TODO if pawn was jump, set it to enpassant pawn
        if self.movedPiece.toString() == 'P':
            if self.movedPiece.position+16 == self.destination:
                print("Black j")
                newBoard.enPassPawn = updatePiece
                newBoard.enPassPawnBehind = self.movedPiece.position+8
        elif self.movedPiece.toString() == 'p':
            if self.movedPiece.position-16 == self.destination:
                print("White j")
                newBoard.enPassPawn = updatePiece
                newBoard.enPassPawnBehind = self.movedPiece.position-8







        return newBoard







