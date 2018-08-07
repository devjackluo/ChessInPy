import copy
from board.chessBoard import Board
from board.tile import Tile
from pieces import nullPiece
from pieces import queen
from pieces import rook
import time


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

        # IF THERE WAS AN ENPASSANT PAWN AND WE USED A PAWN TO ATTACK IT'S SQUARE
        # SET A MARKED FOR IT FOR IT TO BE SKIPPED
        enpassLocation = None
        if self.movedPiece.toString() == 'P':
            if not self.board.enPassPawn == None:
                if self.destination == self.board.enPassPawnBehind:
                    enpassLocation = self.board.enPassPawn.position
        elif self.movedPiece.toString() == 'p':
            if not self.board.enPassPawn == None:
                if self.destination == self.board.enPassPawnBehind:
                    enpassLocation = self.board.enPassPawn.position

        # FILL NEW BOARD WITH EVERYTHING EXCEPT DESTINATION, CURRENT LOCATION AND ENPASS LOCATION
        # ELSE FILL IT WITH A NULL PIECE FOR NOW
        for tile in range(64):
            if not tile == self.movedPiece.position and not tile == self.destination and not tile == enpassLocation:
                gameTiles[tile] = self.board.gameTiles[tile]
            else:
                gameTiles[tile] = Tile(tile, nullPiece.NullPiece())

        # IF WE CASTLED, REPLACE THE ROOK WITH A NULL AND MOVE IT TO CORRECT POSITION
        if self.movedPiece.toString() == 'K' and self.movedPiece.firstMove:
            if self.destination == 2:
                if self.board.gameTiles[0].pieceOnTile.toString() == "R" \
                        and self.board.gameTiles[0].pieceOnTile.firstMove:

                    gameTiles[0] = Tile(0, nullPiece.NullPiece())
                    gameTiles[3] = Tile(3, rook.Rook("Black", 3))
            elif self.destination == 6:
                if self.board.gameTiles[7].pieceOnTile.toString() == "R" \
                        and self.board.gameTiles[7].pieceOnTile.firstMove:

                    gameTiles[7] = Tile(7, nullPiece.NullPiece())
                    gameTiles[5] = Tile(5, rook.Rook("Black", 5))

        # CASTLE FOR WHITE
        elif self.movedPiece.toString() == 'k':
            if self.destination == 58:
                if self.board.gameTiles[56].pieceOnTile.toString() == "r" \
                        and self.board.gameTiles[56].pieceOnTile.firstMove:

                    gameTiles[56] = Tile(56, nullPiece.NullPiece())
                    gameTiles[59] = Tile(59, rook.Rook("White", 59))
            elif self.destination == 62:
                if self.board.gameTiles[63].pieceOnTile.toString() == "r" \
                        and self.board.gameTiles[56].pieceOnTile.firstMove:

                    gameTiles[63] = Tile(63, nullPiece.NullPiece())
                    gameTiles[61] = Tile(61, rook.Rook("White", 61))

        # FINALLY CREATE A COPY OF MOVED PIECE AND ASSIGN IT TO ITS LOCATION
        updatePiece = copy.copy(self.movedPiece)
        updatePiece.firstMove = False
        updatePiece.position = self.destination
        gameTiles[self.destination] = Tile(self.destination, updatePiece)
        # THEN ASSIGN NEW BOARD'S TILES AS NEW TILES
        newBoard.gameTiles = gameTiles

        # IT WAS A PAWN JUMP MOVE, ASSIGN IT TO BE THE ENPASS PAWN AND SET IT'S LOCATION BEHIND IT
        if self.movedPiece.toString() == 'P':
            if self.movedPiece.position + 16 == self.destination:
                newBoard.enPassPawn = updatePiece
                newBoard.enPassPawnBehind = self.movedPiece.position + 8
        elif self.movedPiece.toString() == 'p':
            if self.movedPiece.position - 16 == self.destination:
                newBoard.enPassPawn = updatePiece
                newBoard.enPassPawnBehind = self.movedPiece.position - 8

        # IF IT WAS A PAWN MOVE AND IT REACHED THE LAST RANK, REPLACE IT WAS A QUEEN
        if self.movedPiece.toString() == 'P':
            if self.destination in self.movedPiece.eighthRow:
                newBoard.gameTiles[self.destination] = Tile(self.destination, queen.Queen("Black", self.destination))
        elif self.movedPiece.toString() == 'p':
            if self.destination in self.movedPiece.firstRow:
                newBoard.gameTiles[self.destination] = Tile(self.destination, queen.Queen("White", self.destination))

        # SWITCH CURRENT PLAYER OF THE BOARD
        newBoard.currentPlayer = self.board.currentPlayer
        if newBoard.currentPlayer == "White":
            newBoard.currentPlayer = "Black"
        elif newBoard.currentPlayer == "Black":
            newBoard.currentPlayer = "White"

        # WITH THE NEW BOARD CREATED, CHECK IF THE OPPONENT DID A VALID MOVE
        good = self.checkChecks(newBoard)

        if not good:
            return False

        mate = self.checkCheckmateOrStalemate(newBoard, newBoard.currentPlayer)
        if mate:
            return False

        return newBoard

    def checkMateBoard(self):

        newBoard = Board()
        gameTiles = {}

        # IF THERE WAS AN ENPASSANT PAWN AND WE USED A PAWN TO ATTACK IT'S SQUARE
        # SET A MARKED FOR IT FOR IT TO BE SKIPPED
        enpassLocation = None
        if self.movedPiece.toString() == 'P':
            if not self.board.enPassPawn == None:
                if self.destination == self.board.enPassPawnBehind:
                    enpassLocation = self.board.enPassPawn.position
        elif self.movedPiece.toString() == 'p':
            if not self.board.enPassPawn == None:
                if self.destination == self.board.enPassPawnBehind:
                    enpassLocation = self.board.enPassPawn.position

        # FILL NEW BOARD WITH EVERYTHING EXCEPT DESTINATION, CURRENT LOCATION AND ENPASS LOCATION
        # ELSE FILL IT WITH A NULL PIECE FOR NOW
        for tile in range(64):
            if not tile == self.movedPiece.position and not tile == self.destination and not tile == enpassLocation:
                gameTiles[tile] = self.board.gameTiles[tile]
            else:
                gameTiles[tile] = Tile(tile, nullPiece.NullPiece())

        # IF WE CASTLED, REPLACE THE ROOK WITH A NULL AND MOVE IT TO CORRECT POSITION
        if self.movedPiece.toString() == 'K' and self.movedPiece.firstMove:
            if self.destination == 2:
                if self.board.gameTiles[0].pieceOnTile.toString() == "R" \
                        and self.board.gameTiles[0].pieceOnTile.firstMove:

                    gameTiles[0] = Tile(0, nullPiece.NullPiece())
                    gameTiles[3] = Tile(3, rook.Rook("Black", 3))
            elif self.destination == 6:
                if self.board.gameTiles[7].pieceOnTile.toString() == "R" \
                        and self.board.gameTiles[7].pieceOnTile.firstMove:

                    gameTiles[7] = Tile(7, nullPiece.NullPiece())
                    gameTiles[5] = Tile(5, rook.Rook("Black", 5))

        # CASTLE FOR WHITE
        elif self.movedPiece.toString() == 'k':
            if self.destination == 58:
                if self.board.gameTiles[56].pieceOnTile.toString() == "r" \
                        and self.board.gameTiles[56].pieceOnTile.firstMove:

                    gameTiles[56] = Tile(56, nullPiece.NullPiece())
                    gameTiles[59] = Tile(59, rook.Rook("White", 59))
            elif self.destination == 62:
                if self.board.gameTiles[63].pieceOnTile.toString() == "r" \
                        and self.board.gameTiles[56].pieceOnTile.firstMove:

                    gameTiles[63] = Tile(63, nullPiece.NullPiece())
                    gameTiles[61] = Tile(61, rook.Rook("White", 61))

        # FINALLY CREATE A COPY OF MOVED PIECE AND ASSIGN IT TO ITS LOCATION
        updatePiece = copy.copy(self.movedPiece)
        updatePiece.firstMove = False
        updatePiece.position = self.destination
        gameTiles[self.destination] = Tile(self.destination, updatePiece)
        # THEN ASSIGN NEW BOARD'S TILES AS NEW TILES
        newBoard.gameTiles = gameTiles

        # IT WAS A PAWN JUMP MOVE, ASSIGN IT TO BE THE ENPASS PAWN AND SET IT'S LOCATION BEHIND IT
        if self.movedPiece.toString() == 'P':
            if self.movedPiece.position + 16 == self.destination:
                newBoard.enPassPawn = updatePiece
                newBoard.enPassPawnBehind = self.movedPiece.position + 8
        elif self.movedPiece.toString() == 'p':
            if self.movedPiece.position - 16 == self.destination:
                newBoard.enPassPawn = updatePiece
                newBoard.enPassPawnBehind = self.movedPiece.position - 8

        # IF IT WAS A PAWN MOVE AND IT REACHED THE LAST RANK, REPLACE IT WAS A QUEEN
        if self.movedPiece.toString() == 'P':
            if self.destination in self.movedPiece.eighthRow:
                newBoard.gameTiles[self.destination] = Tile(self.destination, queen.Queen("Black", self.destination))
        elif self.movedPiece.toString() == 'p':
            if self.destination in self.movedPiece.firstRow:
                newBoard.gameTiles[self.destination] = Tile(self.destination, queen.Queen("White", self.destination))

        # SWITCH CURRENT PLAYER OF THE BOARD
        newBoard.currentPlayer = self.board.currentPlayer
        if newBoard.currentPlayer == "White":
            newBoard.currentPlayer = "Black"
        elif newBoard.currentPlayer == "Black":
            newBoard.currentPlayer = "White"

        # WITH THE NEW BOARD CREATED, CHECK IF THE OPPONENT DID A VALID MOVE
        good = self.checkChecks(newBoard)

        if not good:
            return False

        return newBoard

    def checkChecks(self, newBoard):

        # AFTER MY OPPONENT MOVED AND HE IS STILL IN CHECK, OBVIOUSLY MEANS IT WAS BOT A LEGAL MOVE
        if newBoard.currentPlayer == "White":
            enemyKing = None
            for sq in range(len(newBoard.gameTiles)):
                if newBoard.gameTiles[sq].pieceOnTile.toString() == "K":
                    enemyKing = newBoard.gameTiles[sq].pieceOnTile.position
                    break

            myPieces = newBoard.calculateActivePieces("White")

            for piece in myPieces:
                pieceLegals = piece.calculateLegalMoves(newBoard)
                for legals in pieceLegals:
                    if legals == enemyKing:
                        return False

        else:

            enemyKing = None
            for sq in range(len(newBoard.gameTiles)):
                if newBoard.gameTiles[sq].pieceOnTile.toString() == "k":
                    enemyKing = newBoard.gameTiles[sq].pieceOnTile.position

            myPieces = newBoard.calculateActivePieces("Black")

            for piece in myPieces:
                pieceLegals = piece.calculateLegalMoves(newBoard)
                for legals in pieceLegals:
                    if legals == enemyKing:
                        return False

        return True

    @staticmethod
    def checkCheckmateOrStalemate(board, alliance):
        pieces = board.calculateActivePieces(alliance)
        moves = board.calculateLegalMoves(pieces, board)

        for myMoves in moves:
            makeMove = Move(board, myMoves[1], myMoves[0])
            newboard = makeMove.checkMateBoard()
            if newboard is not False:
                return False

        return True
