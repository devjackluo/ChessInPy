from board.move import Move
from player.boardEvaluator import BoardEvaluator
import sys

class Minimax:

    board = None
    depth = None
    boardEvaluator = None
    currentValue = None
    highestSeenValue = None
    lowestSeenValue = None
    bestMove = None

    def __init__(self, board, depth):
        self.board = board
        self.depth = depth
        self.boardEvaluator = BoardEvaluator()

    def getMove(self):

        currentPlayer = self.board.currentPlayer
        myPieces = self.board.calculateActivePieces(currentPlayer)
        allLegals = self.board.calculateLegalMoves(myPieces, self.board)

        self.highestSeenValue = -sys.maxsize
        self.lowestSeenValue = sys.maxsize

        for myMoves in allLegals:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.createNewBoard()
            if newboard is not False:

                if currentPlayer == "White":
                    self.currentValue = self.min(newboard, self.depth)
                else:
                    self.currentValue = self.max(newboard, self.depth)

                if currentPlayer == "White" and self.currentValue > self.highestSeenValue:
                    self.highestSeenValue = self.currentValue
                    self.bestMove = newboard
                if currentPlayer == "Black" and self.currentValue < self.lowestSeenValue:
                    self.lowestSeenValue = self.currentValue
                    self.bestMove = newboard

        return self.bestMove

    def max(self, board, depth):

        # TODO checkmate/stalemate
        if depth == 0 and not Move.checkCheckmateOrStalemate(board, board.currentPlayer):
            return self.boardEvaluator.evaluate(board, depth)

        highestSeenValue = -sys.maxsize
        myPieces = board.calculateActivePieces(board.currentPlayer)
        allLegals = board.calculateLegalMoves(myPieces, board)

        for myMoves in allLegals:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.createNewBoard()
            if not newboard == False:
                value = self.min(newboard, depth - 1)
                if value >= highestSeenValue:
                    highestSeenValue = value

        return highestSeenValue

    def min(self, board, depth):

        # TODO checkmate/stalemate
        if depth == 0 and not Move.checkCheckmateOrStalemate(board, board.currentPlayer):
            return self.boardEvaluator.evaluate(board, depth)

        lowestSeenValue = sys.maxsize
        myPieces = board.calculateActivePieces(board.currentPlayer)
        allLegals = board.calculateLegalMoves(myPieces, board)

        for myMoves in allLegals:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.createNewBoard()
            if not newboard == False:
                value = self.min(newboard, depth - 1)
                if value <= lowestSeenValue:
                    lowestSeenValue = value

        return lowestSeenValue
