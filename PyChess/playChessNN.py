import pygame
from board import chessBoard
from board.move import Move
import subprocess


pygame.init()
gameDisplay = pygame.display.set_mode((800, 800))
pygame.display.set_caption("PyChess")
clock = pygame.time.Clock()

firstBoard = chessBoard.Board()
firstBoard.createBoard()

allTiles = []
allPieces = []
currentPlayer = firstBoard.currentPlayer


def createSqParams():
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


def squares(x, y, w, h, color):
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])
    allTiles.append([color, [x, y, w, h]])


def drawChessPieces():
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
                squares(xpos, ypos, width, height, white)
                if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                    img = pygame.image.load(
                        "./ChessArt/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() +
                        firstBoard.gameTiles[
                            number].pieceOnTile.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    allPieces.append([img, [xpos, ypos], firstBoard.gameTiles[number].pieceOnTile])
                xpos += 100
            else:
                squares(xpos, ypos, width, height, black)
                if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                    img = pygame.image.load(
                        "./ChessArt/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() +
                        firstBoard.gameTiles[
                            number].pieceOnTile.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    allPieces.append([img, [xpos, ypos], firstBoard.gameTiles[number].pieceOnTile])
                xpos += 100

            color += 1
            number += 1
        color += 1
        xpos = 0
        ypos += 100


def updateChessPieces():
    xpos = 0
    ypos = 0
    number = 0
    newPieces = []

    for _ in range(8):
        for _ in range(8):
            if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                img = pygame.image.load(
                    "./ChessArt/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() + firstBoard.gameTiles[
                        number].pieceOnTile.toString().upper() + ".png")
                img = pygame.transform.scale(img, (100, 100))

                newPieces.append([img, [xpos, ypos], firstBoard.gameTiles[number].pieceOnTile])
            xpos += 100
            number += 1
        xpos = 0
        ypos += 100

    return newPieces


def decodePiece(val):
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



def decodeFile(val):
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


def decodeRank(val):
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


allSqParams = createSqParams()
drawChessPieces()

selectedImage = None
selectedLegals = None
resetColors = []
quitGame = False
mx, my = pygame.mouse.get_pos()
prevx, prevy = [0, 0]


while not quitGame:

    for event in pygame.event.get():

        # HANDLE QUIT GAME
        if event.type == pygame.QUIT:
            quitGame = True
            pygame.quit()
            quit()

        # HANDLE SELECTING PIECE AND THEIR LEGAL MOVES
        # ONLY WHEN NO PIECE IS SELECTED YET
        if event.type == pygame.MOUSEBUTTONDOWN:

            if selectedImage == None:
                mx, my = pygame.mouse.get_pos()
                for piece in range(len(allPieces)):
                    if allPieces[piece][2].alliance == currentPlayer:
                        if allPieces[piece][1][0] < mx < allPieces[piece][1][0] + 100:
                            if allPieces[piece][1][1] < my < allPieces[piece][1][1] + 100:
                                selectedImage = piece
                                prevx = allPieces[piece][1][0]
                                prevy = allPieces[piece][1][1]
                                selectedLegals = allPieces[selectedImage][2].calculateLegalMoves(firstBoard)
                                for legals in selectedLegals:
                                    resetColors.append([legals, allTiles[legals][0]])
                                    if allTiles[legals][0] == (66, 134, 244):
                                        allTiles[legals][0] = (135, 46, 40)
                                    else:
                                        allTiles[legals][0] = (183, 65, 56)

        # HANDLE DRAGGING PIECE
        if event.type == pygame.MOUSEMOTION and not selectedImage == None:
            mx, my = pygame.mouse.get_pos()
            allPieces[selectedImage][1][0] = mx - 50
            allPieces[selectedImage][1][1] = my - 50

        # HANDLE LETTING GO ON PIECE TO THEIR MOVED SPOT
        if event.type == pygame.MOUSEBUTTONUP:

            if not selectedImage == None:

                for resets in resetColors:
                    allTiles[resets[0]][0] = resets[1]

                try:

                    pieceMoves = allPieces[selectedImage][2].calculateLegalMoves(firstBoard)
                    legal = False
                    theMove = 0
                    for moveDes in pieceMoves:
                        if allSqParams[moveDes][0] < allPieces[selectedImage][1][0] + 50 < allSqParams[moveDes][1]:
                            if allSqParams[moveDes][2] < allPieces[selectedImage][1][1] + 50 < allSqParams[moveDes][3]:
                                legal = True
                                theMove = moveDes

                    if legal == False:
                        allPieces[selectedImage][1][0] = prevx
                        allPieces[selectedImage][1][1] = prevy
                    else:
                        allPieces[selectedImage][1][0] = allSqParams[theMove][0]
                        allPieces[selectedImage][1][1] = allSqParams[theMove][2]

                        thisMove = Move(firstBoard, allPieces[selectedImage][2], theMove)
                        newBoard = thisMove.createNewBoard()
                        if not newBoard == False:
                            firstBoard = newBoard

                        newP = updateChessPieces()
                        allPieces = newP

                        currentPlayer = newBoard.currentPlayer

                        boardString = ' '.join(str(x) for x in newBoard.getBoardArr())

                        result = subprocess.check_output(["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictPieceScript.py", boardString])
                        decodePiece(result.decode("utf-8").replace("\r", "").replace("\n", ""))

                        result = subprocess.check_output(["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictFileScript.py", boardString])
                        decodeFile(result.decode("utf-8").replace("\r", "").replace("\n", ""))

                        result = subprocess.check_output(["python", "C:\\Users\\Jack\\Documents\\GitHub\\ChessInPy\\PyChess\\chessNN\\predictRankScript.py", boardString])
                        decodeRank(result.decode("utf-8").replace("\r", "").replace("\n", ""))



                except:
                    pass

                prevy = 0
                prevx = 0
                selectedImage = None

    # HANDLE DRAWING TILES EACH FRAME
    for info in allTiles:
        pygame.draw.rect(gameDisplay, info[0], info[1])

    # HANDLE DRAWING PIECES EACH FRAME
    for img in allPieces:
        gameDisplay.blit(img[0], img[1])

    # GAME LOOP MANAGEMENT
    pygame.display.update()
    clock.tick(60)



