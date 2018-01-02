from chessBoard import Board
from move import Move
from boardEvaluator import BoardEvaluator

class Minimax:

    board = None
    depth = None
    boardEvaluator = None

    def __init__(self, board, depth):
        self.board = board
        self.depth = depth
        self.boardEvaluator = BoardEvaluator()

    def getMove(self):

        #nBoard = Board()
        #nBoard.printBoard()

        currentPlayer = self.board.currentPlayer
        #print(currentPlayer)

        myPieces = self.board.calculateActivePieces(currentPlayer)
        allLegals = self.board.calculateLegalMoves(myPieces, self.board)

        #print(allLegals)

        bestMove = None
        highestSeenValue = -1000000
        lowestSeenValue = 1000000
        currentValue = None

        #print(self.depth)

        for myMoves in allLegals:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.createNewBoard()
            if not newboard == False:
                if currentPlayer == "White":
                    #print("Work w")
                    currentValue = self.min(newboard, self.depth)
                    #print(currentValue)
                else:
                    #print("Work b")
                    currentValue = self.max(newboard, self.depth)
                    #print(currentValue)

                if currentPlayer == "White" and currentValue > highestSeenValue:
                    highestSeenValue = currentValue
                    bestMove = newboard

                if currentPlayer == "Black" and currentValue < lowestSeenValue:
                    lowestSeenValue = currentValue
                    bestMove = newboard

        return bestMove



    def max(self, board, depth):

        #TODO checkmate/stalemate
        if depth == 0:
            #print("Hello")
            #return 99
            return self.boardEvaluator.evaluate(board, depth)

        #self.min(board, depth-1)

        highestSeenValue = -1000000
        myPieces = board.calculateActivePieces(board.currentPlayer)
        allLegals = board.calculateLegalMoves(myPieces, board)

        for myMoves in allLegals:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.createNewBoard()
            if not newboard == False:
                value = self.min(newboard, depth-1)
                if value >= highestSeenValue:
                    highestSeenValue = value

        return highestSeenValue


    def min(self, board, depth):

        # TODO checkmate/stalemate
        if depth == 0:
            return self.boardEvaluator.evaluate(board, depth)

        #self.max(board, depth-1)

        lowestSeenValue = 1000000
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






