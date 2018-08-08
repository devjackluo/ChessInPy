import pygame
from board import chessBoard
from board.move import Move
import subprocess
import threading

class playChessNN():

    gameDisplay = None
    clock = None

    firstBoard = None
    allTiles = None
    allPieces = None
    currentPlayer = None
    allSqParams = None

    selectedImage = None
    selectedLegals = None
    resetColors = None
    quitGame = None
    mx = None
    my = None
    prevx = None
    prevy = None

    nnThinking = None
    nnSquareColors = None
    movesSquareColors = None

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("PyChess")
        self.clock = pygame.time.Clock()

        self.firstBoard = chessBoard.Board()
        self.firstBoard.createBoard()

        self.allTiles = []
        self.allPieces = []
        self.currentPlayer = self.firstBoard.currentPlayer

        self.allSqParams = self.createSqParams()
        self.drawChessPieces()

        self.selectedImage = None
        self.selectedLegals = None
        self.resetColors = []
        self.quitGame = False
        self.mx, self.my = pygame.mouse.get_pos()
        self.prevx, self.prevy = [0, 0]

        self.nnThinking = False
        self.nnSquareColors = []
        self.movesSquareColors = []

        thread = threading.Thread(target=self.backgroundNN, args=[self.firstBoard])
        thread.start()

        while not self.quitGame:

            for event in pygame.event.get():

                # HANDLE QUIT GAME
                if event.type == pygame.QUIT:
                    self.quitGame = True
                    pygame.quit()
                    quit()

                # HANDLE SELECTING PIECE AND THEIR LEGAL MOVES
                # ONLY WHEN NO PIECE IS SELECTED YET
                if event.type == pygame.MOUSEBUTTONDOWN and not self.nnThinking:

                    if self.selectedImage == None:
                        self.mx, self.my = pygame.mouse.get_pos()
                        for piece in range(len(self.allPieces)):
                            if self.allPieces[piece][2].alliance == self.currentPlayer:
                                if self.allPieces[piece][1][0] < self.mx < self.allPieces[piece][1][0] + 100:
                                    if self.allPieces[piece][1][1] < self.my < self.allPieces[piece][1][1] + 100:
                                        self.selectedImage = piece
                                        self.prevx = self.allPieces[piece][1][0]
                                        self.prevy = self.allPieces[piece][1][1]
                                        self.selectedLegals = self.allPieces[self.selectedImage][2].calculateLegalMoves(self.firstBoard)
                                        for legals in self.selectedLegals:
                                            self.resetColors.append([legals, self.allTiles[legals][0]])
                                            if self.allTiles[legals][0] == (66, 134, 244) \
                                                    or self.allTiles[legals][0] == (29, 81, 39) \
                                                    or self.allTiles[legals][0] == (86, 32, 130)\
                                                    or self.allTiles[legals][0] == (226, 0, 0):
                                                self.allTiles[legals][0] = (135, 46, 40)
                                            else:
                                                self.allTiles[legals][0] = (183, 65, 56)

                # HANDLE DRAGGING PIECE
                if event.type == pygame.MOUSEMOTION and not self.selectedImage == None and not self.nnThinking:
                    self.mx, self.my = pygame.mouse.get_pos()
                    self.allPieces[self.selectedImage][1][0] = self.mx - 50
                    self.allPieces[self.selectedImage][1][1] = self.my - 50

                # HANDLE LETTING GO ON PIECE TO THEIR MOVED SPOT
                if event.type == pygame.MOUSEBUTTONUP and not self.nnThinking:

                    if not self.selectedImage == None:

                        for resets in self.resetColors:
                            self.allTiles[resets[0]][0] = resets[1]
                            #self.resetColors.remove(resets)
                        self.resetColors = []

                        try:

                            pieceMoves = self.allPieces[self.selectedImage][2].calculateLegalMoves(self.firstBoard)
                            legal = False
                            theMove = 0
                            for moveDes in pieceMoves:
                                if self.allSqParams[moveDes][0] < self.allPieces[self.selectedImage][1][0] + 50 < self.allSqParams[moveDes][1]:
                                    if self.allSqParams[moveDes][2] < self.allPieces[self.selectedImage][1][1] + 50 < \
                                            self.allSqParams[moveDes][3]:
                                        legal = True
                                        theMove = moveDes

                            if legal == False:
                                self.allPieces[self.selectedImage][1][0] = self.prevx
                                self.allPieces[self.selectedImage][1][1] = self.prevy
                            else:
                                self.allPieces[self.selectedImage][1][0] = self.allSqParams[theMove][0]
                                self.allPieces[self.selectedImage][1][1] = self.allSqParams[theMove][2]

                                thisMove = Move(self.firstBoard, self.allPieces[self.selectedImage][2], theMove)
                                newBoard = thisMove.createNewBoard()
                                if not newBoard == False:
                                    self.firstBoard = newBoard

                                newP = self.updateChessPieces()
                                self.allPieces = newP

                                self.currentPlayer = newBoard.currentPlayer

                                for resets in self.movesSquareColors:
                                    self.allTiles[resets[0]][0] = resets[1]
                                self.movesSquareColors = []

                                # HANDLE GETTING NN RESPONSE
                                for resets in self.nnSquareColors:
                                    self.allTiles[resets[0]][0] = resets[1]
                                self.nnSquareColors = []

                                thread = threading.Thread(target=self.backgroundNN, args=[newBoard])
                                thread.start()
                                # thread.join()





                        except:
                            pass

                        self.prevy = 0
                        self.prevx = 0
                        self.selectedImage = None

            # HANDLE DRAWING TILES EACH FRAME
            for info in self.allTiles:
                pygame.draw.rect(self.gameDisplay, info[0], info[1])

            # HANDLE DRAWING PIECES EACH FRAME
            for img in self.allPieces:
                self.gameDisplay.blit(img[0], img[1])

            # GAME LOOP MANAGEMENT
            pygame.display.update()
            self.clock.tick(60)




    def createSqParams(self):
        allSqRanges = []
        xMin = 0
        xMax = 100
        yMin = 0
        yMax = 100
        for _ in range(8):
            for _ in range(8):
                allSqRanges.append([xMin, xMax, yMin, yMax])
                xMin += 100
                xMax += 100
            xMin = 0
            xMax = 100
            yMin += 100
            yMax += 100
        return allSqRanges


    def squares(self, x, y, w, h, color):
        pygame.draw.rect(self.gameDisplay, color, [x, y, w, h])
        self.allTiles.append([color, [x, y, w, h]])


    def drawChessPieces(self):
        xpos = 0
        ypos = 0
        color = 0
        width = 100
        height = 100
        black = (66, 134, 244)
        white = (143, 155, 175)
        number = 0
        for _ in range(8):
            for _ in range(8):
                if color % 2 == 0:
                    self.squares(xpos, ypos, width, height, white)
                    if not self.firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                        img = pygame.image.load(
                            "./ChessArt/" + self.firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() +
                            self.firstBoard.gameTiles[
                                number].pieceOnTile.toString().upper() + ".png")
                        img = pygame.transform.scale(img, (100, 100))
                        self.allPieces.append([img, [xpos, ypos], self.firstBoard.gameTiles[number].pieceOnTile])
                    xpos += 100
                else:
                    self.squares(xpos, ypos, width, height, black)
                    if not self.firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                        img = pygame.image.load(
                            "./ChessArt/" + self.firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() +
                            self.firstBoard.gameTiles[
                                number].pieceOnTile.toString().upper() + ".png")
                        img = pygame.transform.scale(img, (100, 100))
                        self.allPieces.append([img, [xpos, ypos], self.firstBoard.gameTiles[number].pieceOnTile])
                    xpos += 100

                color += 1
                number += 1
            color += 1
            xpos = 0
            ypos += 100


    def updateChessPieces(self):
        xpos = 0
        ypos = 0
        number = 0
        newPieces = []

        for _ in range(8):
            for _ in range(8):
                if not self.firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                    img = pygame.image.load(
                        "./ChessArt/" + self.firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() + self.firstBoard.gameTiles[
                            number].pieceOnTile.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))

                    newPieces.append([img, [xpos, ypos], self.firstBoard.gameTiles[number].pieceOnTile])
                xpos += 100
                number += 1
            xpos = 0
            ypos += 100

        return newPieces


    def decodePiece(self, val):
        #print(val)
        arr = list(val)
        for piece in arr:
            if piece == "1":
                print("Maybe move King?")
            elif piece == "2":
                print("Maybe move Queen?")
            elif piece == "3":
                print("Maybe move Rook?")
            elif piece == "4":
                print("Maybe move Bishop?")
            elif piece == "5":
                print("Maybe move Knight?")
            elif piece == "6":
                print("Maybe move Pawn?")


    def decodeFile(self, val):
        arr = list(val)
        for file in arr:
            if file == "1":
                print("Think around A file?")
            elif file == "2":
                print("Think around B file?")
            elif file == "3":
                print("Think around C file?")
            elif file == "4":
                print("Think around D file?")
            elif file == "5":
                print("Think around E file?")
            elif file == "6":
                print("Think around F file?")
            elif file == "7":
                print("Think around G file?")
            elif file == "8":
                print("Think around H file?")


    def decodeRank(self, val):
        arr = list(val)
        for rank in arr:
            if rank == "1":
                print("What about 1th rank?")
            elif rank == "2":
                print("What about 2th rank?")
            elif rank == "3":
                print("What about 3th rank?")
            elif rank == "4":
                print("What about 4th rank?")
            elif rank == "5":
                print("What about 5th rank?")
            elif rank == "6":
                print("What about 6th rank?")
            elif rank == "7":
                print("What about 7th rank?")
            elif rank == "8":
                print("What about 8th rank?")

    def colorFileRank(self, file, rank):
        files = list(file)
        ranks = list(rank)

        # print(files)
        # print(ranks)

        #print((int(file[0])-1)+((8-int(rank[0]))*8))
        #print(((8-int(rank[0]))*8))

        for f in files:
            for r in ranks:
                position = (int(f) - 1) + ((8 - int(r)) * 8)
                self.nnSquareColors.append([position, self.allTiles[position][0]])
                if self.allTiles[position][0] == (66, 134, 244):
                    self.allTiles[position][0] = (29, 81, 39)
                else:
                    self.allTiles[position][0] = (48, 135, 65)


        #self.allTiles[][0] = (100, 65, 56)

        # for tile in range(len(self.allTiles)):
        #     #self.resetColors.append([tile, self.allTiles[tile][0]])
        #     # if self.allTiles[legals][0] == (66, 134, 244):
        #     #     self.allTiles[legals][0] = (135, 46, 40)
        #     # else:
        #     #     self.allTiles[legals][0] = (183, 65, 56)
        #     self.allTiles[tile][0] = (100, 65, 56)

    def backgroundNN(self, board):

        self.nnThinking = True
        print("NN IS THINKING....")

        boardString = ' '.join(str(x) for x in board.getBoardArr())

        pieceResult = subprocess.check_output(
            ["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictPieceScript.py",
             boardString])
        self.decodePiece(pieceResult.decode("utf-8").replace("\r", "").replace("\n", ""))

        fileResult = subprocess.check_output(
            ["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictFileScript.py",
             boardString])
        fileToString = fileResult.decode("utf-8").replace("\r", "").replace("\n", "")
        self.decodeFile(fileToString)

        rankResult = subprocess.check_output(
            ["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictRankScript.py",
             boardString])
        rankToString = rankResult.decode("utf-8").replace("\r", "").replace("\n", "")
        self.decodeRank(rankToString)

        self.colorFileRank(fileToString, rankToString)

        self.nnThinking = False

        #self.predictOkMove()

    def predictOkMove(self):

        self.nnThinking = True

        myPieces = self.firstBoard.calculateActivePieces(self.firstBoard.currentPlayer)
        allLegals = self.firstBoard.calculateLegalMoves(myPieces, self.firstBoard)

        #boardString = ' '.join(str(x) for x in self.firstBoard.getBoardArrSide())

        allBoardStrings = ""

        validMoves = []

        for myMoves in allLegals:
            makeMove = Move(self.firstBoard, myMoves[1], myMoves[0])
            newboard = makeMove.createNewBoard()
            if newboard is not False:
                validMoves.append(makeMove)
                boardString = ' '.join(str(x) for x in newboard.getBoardArrSide())
                allBoardStrings += boardString + "\n"
                # sideResult = subprocess.check_output(
                #     ["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictOkMoveScript.py",
                #      boardString])
                # sideToString = sideResult.decode("utf-8").replace("\r", "").replace("\n", "")
                # print(sideToString)

        #print(allBoardStrings)

        sideResult = subprocess.check_output(
            ["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictOkMoveScript.py",
             allBoardStrings])
        sideToString = sideResult.decode("utf-8").replace("\r", "").replace("\n", "")

        print(sideToString)

        arr = list(sideToString)
        currentP = self.firstBoard.currentPlayer
        square = []
        for i in range(len(arr)):
            if currentP == "White":
                if arr[i] == "0":
                    print(validMoves[i].movedPiece.toString(), validMoves[i].destination)
                    if validMoves[i].destination not in square:
                        square.append(validMoves[i].destination)
            elif currentP == "Black":
                if arr[i] == "1":
                    print(validMoves[i].movedPiece.toString(), validMoves[i].destination)
                    if validMoves[i].destination not in square:
                        square.append(validMoves[i].destination)

        # inputs = allBoardStrings.split('\n')
        # for i in range(len(inputs)-1):
        #     print(inputs[i])
        #print(allBoardStrings)

        self.colorGoodMoves(square)

        self.nnThinking = False

    def colorGoodMoves(self, squares):

        for s in squares:
            self.movesSquareColors.append([s, self.allTiles[s][0]])
            if self.allTiles[s][0] == (66, 134, 244):
                self.allTiles[s][0] = (86, 32, 130)
            elif self.allTiles[s][0] == (143, 155, 175):
                self.allTiles[s][0] = (124, 50, 186)
            elif self.allTiles[s][0] == (29, 81, 39):
                self.allTiles[s][0] = (226, 0, 0)
            elif self.allTiles[s][0] == (48, 135, 65):
                self.allTiles[s][0] = (226, 72, 72)

playChessNN()

