import pygame
from board import chessBoard
from board.move import Move
import threading
from player.minimax import Minimax


class playChessNew():
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

    aiBoard = None

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

        self.aiBoard = False

        while not self.quitGame:

            for event in pygame.event.get():

                # HANDLE QUIT GAME
                if event.type == pygame.QUIT:
                    self.quitGame = True
                    pygame.quit()
                    quit()

                # HANDLE SELECTING PIECE AND THEIR LEGAL MOVES
                # ONLY WHEN NO PIECE IS SELECTED YET
                if event.type == pygame.MOUSEBUTTONDOWN and not self.aiBoard:

                    if self.selectedImage == None:
                        self.mx, self.my = pygame.mouse.get_pos()
                        for piece in range(len(self.allPieces)):
                            if self.allPieces[piece][2].alliance == self.currentPlayer:
                                if self.allPieces[piece][1][0] < self.mx < self.allPieces[piece][1][0] + 100:
                                    if self.allPieces[piece][1][1] < self.my < self.allPieces[piece][1][1] + 100:
                                        self.selectedImage = piece
                                        self.prevx = self.allPieces[piece][1][0]
                                        self.prevy = self.allPieces[piece][1][1]
                                        self.selectedLegals = self.allPieces[self.selectedImage][2].calculateLegalMoves(
                                            self.firstBoard)
                                        for legals in self.selectedLegals:
                                            self.resetColors.append([legals, self.allTiles[legals][0]])
                                            if self.allTiles[legals][0] == (66, 134, 244) or self.allTiles[legals][
                                                0] == (29, 81, 39):
                                                self.allTiles[legals][0] = (135, 46, 40)
                                            else:
                                                self.allTiles[legals][0] = (183, 65, 56)

                # HANDLE DRAGGING PIECE
                if event.type == pygame.MOUSEMOTION and not self.selectedImage == None and not self.aiBoard:
                    self.mx, self.my = pygame.mouse.get_pos()
                    self.allPieces[self.selectedImage][1][0] = self.mx - 50
                    self.allPieces[self.selectedImage][1][1] = self.my - 50

                # HANDLE LETTING GO ON PIECE TO THEIR MOVED SPOT
                if event.type == pygame.MOUSEBUTTONUP and not self.aiBoard:

                    if not self.selectedImage == None:

                        for resets in self.resetColors:
                            self.allTiles[resets[0]][0] = resets[1]
                            # self.resetColors.remove(resets)

                        try:

                            pieceMoves = self.allPieces[self.selectedImage][2].calculateLegalMoves(self.firstBoard)
                            legal = False
                            theMove = 0
                            for moveDes in pieceMoves:
                                if self.allSqParams[moveDes][0] < self.allPieces[self.selectedImage][1][0] + 50 < \
                                        self.allSqParams[moveDes][1]:
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

                                thread = threading.Thread(target=self.miniMaxMove, args=[])
                                thread.start()


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
                        "./ChessArt/" + self.firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() +
                        self.firstBoard.gameTiles[
                            number].pieceOnTile.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))

                    newPieces.append([img, [xpos, ypos], self.firstBoard.gameTiles[number].pieceOnTile])
                xpos += 100
                number += 1
            xpos = 0
            ypos += 100

        return newPieces

    def miniMaxMove(self):

        if self.currentPlayer == "Black":
            print("Black AI is Thinking...")
            self.aiBoard = True
            minimax = Minimax(self.firstBoard, 1)
            self.aiBoard = minimax.getMove()
            self.firstBoard = self.aiBoard
            newP = self.updateChessPieces()
            self.allPieces = newP
            self.currentPlayer = self.aiBoard.currentPlayer
            self.aiBoard = False

        # if self.currentPlayer == "White":
        #     print("White AI is Thinking...")
        #     self.aiBoard = True
        #     minimax = Minimax(self.firstBoard, 1)
        #     self.aiBoard = minimax.getMove()
        #     self.firstBoard = self.aiBoard
        #     newP = self.updateChessPieces()
        #     self.allPieces = newP
        #     self.currentPlayer = self.aiBoard.currentPlayer
        #     self.aiBoard = False


playChessNew()
