import pygame
import chessBoard

pygame.init()
gameDisplay = pygame.display.set_mode((800, 800))
pygame.display.set_caption("PyChess")

clock = pygame.time.Clock()


firstBoard = chessBoard.Board()
firstBoard.createBoard()
firstBoard.printBoard()


def squares(x, y, w, h, color):
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])


def drawChessPieces():

    xpos = 0
    ypos = 0
    row = 0
    color = 0
    width = 100
    height = 100
    black = (66,134,244)
    white = (143,155,175)
    number = 0

    for _ in range(8):

        for _ in range(8):
            if color % 2 == 0:
                squares(xpos, ypos, width, height, white)

                if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                    img = pygame.image.load("./ChessArt/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() + firstBoard.gameTiles[
                        number].pieceOnTile.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    gameDisplay.blit(img, (xpos, ypos))

                xpos += 100
            else:

                squares(xpos, ypos, width, height, black)

                if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                    img = pygame.image.load("./ChessArt/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() + firstBoard.gameTiles[
                        number].pieceOnTile.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    gameDisplay.blit(img, (xpos, ypos))

                xpos += 100

            #print(firstBoard.gameTiles[number].pieceOnTile.toString())


            color += 1
            number += 1


        color += 1
        xpos = 0
        ypos += 100



drawChessPieces()




quitGame = False

while not quitGame:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quitGame = True
            pygame.quit()
            quit()


    pygame.display.update()
    clock.tick(10)

