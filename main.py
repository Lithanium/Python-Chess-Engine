import pygame
import gamestate
import random
import time
import copy
import sys

# Settings
players = 1  # How many people are playing this game
playingWhite = 1  # If single player, which start
normalStart = 1

originalBoard = [
    [-7, -3, -4, -10, -100, -4, -3, -7],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [7, 3, 4, 10, 100, 4, 3, 7]
]

startPos = [
    [-7, -3, -4, 0, -100, 0, 0, 0],
    [0, -1, -1, 0, -1, 0, -1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 1, 0],
    [7, 3, 4, 10, 100, 4, 3, 7]
]


# display setup
pygame.init()
font = pygame.font.SysFont('Times New Roman', 70)
screen = pygame.display.set_mode((512, 576))

if True:
    # Image Setup
    chessboard = pygame.image.load("chessboard.png")
    chessboard = pygame.transform.scale(chessboard, (512, 512))

    bB = pygame.image.load("black-bishop.png")
    bK = pygame.image.load("black-king.png")
    bN = pygame.image.load("black-knight.png")
    bP = pygame.image.load("black-pawn.png")
    bQ = pygame.image.load("black-queen.png")
    bR = pygame.image.load("black-rook.png")
    bB = pygame.transform.scale(bB, (64, 64))
    bK = pygame.transform.scale(bK, (64, 64))
    bN = pygame.transform.scale(bN, (64, 64))
    bP = pygame.transform.scale(bP, (64, 64))
    bQ = pygame.transform.scale(bQ, (64, 64))
    bR = pygame.transform.scale(bR, (64, 64))
    frame = pygame.image.load("user_select.png")
    frame = pygame.transform.scale(frame, (65, 64))
    frame2 = pygame.image.load("bot_select.png")
    frame2 = pygame.transform.scale(frame2, (65, 64))

    wB = pygame.image.load("white-bishop.png")
    wK = pygame.image.load("white-king.png")
    wN = pygame.image.load("white-knight.png")
    wP = pygame.image.load("white-pawn.png")
    wQ = pygame.image.load("white-queen.png")
    wR = pygame.image.load("white-rook.png")
    wB = pygame.transform.scale(wB, (64, 64))
    wK = pygame.transform.scale(wK, (64, 64))
    wN = pygame.transform.scale(wN, (64, 64))
    wP = pygame.transform.scale(wP, (64, 64))
    wQ = pygame.transform.scale(wQ, (64, 64))
    wR = pygame.transform.scale(wR, (64, 64))

    stalemate = font.render("Stalemate", False, (150, 0, 0))
    whiteWin = font.render("White Wins", False, (150, 0, 0))
    blackWin = font.render("Black Wins", False, (150, 0, 0))

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(0, 0, 0), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

# Variable Setup
running = True
if normalStart:
    chessgame = gamestate.Game(originalBoard)
else:
    chessgame = gamestate.Game(startPos)
squareSelect = ()
squareClick = []
chessgame.basicChecks()

# Actual Code
while running:
    # Draw the chessboard
    fromX, fromY = chessgame.botFrom
    legalMoves = chessgame.generateMoves()
    if not chessgame.gameOver:
        # Check for Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                row = loc[0]//64
                col = loc[1]//64
                if col == 8:
                    print("\nDEBUG LOG\n----------\n")
                    chessgame.debug()
                    continue
                if squareSelect == (row, col):
                    squareSelect = ()
                    squareClick = []
                else:
                    squareSelect = (row, col)
                    squareClick.append(squareSelect)
                if len(squareClick) == 2 and (playingWhite == chessgame.whiteMove or players == 2) and players >= 1:
                    revert = copy.deepcopy(chessgame.board)
                    b, a = squareClick[0]
                    y, x = squareClick[1]
                    castling = 0
                    if chessgame.board[a][b] != 100:
                        chessgame.board[x][y] = chessgame.board[a][b]
                        chessgame.board[a][b] = 0
                        if chessgame.whiteMove and x == 0 and chessgame.board[x][y] == 1:
                            chessgame.board[x][y] = 10
                        elif chessgame.whiteMove == 0 and x == 7 and chessgame.board[x][y] == -1:
                            chessgame.board[x][y] = -10
                    else:
                        if chessgame.whiteMove:
                            a1, b1, c1 = chessgame.castleRightsWhite
                            if x == 7 and y == 2 and a1 and b1:
                                castling = 1
                                chessgame.board[7][2] = 100
                                chessgame.board[7][3] = 7
                                chessgame.board[7][0] = 0
                                chessgame.board[7][1] = 0
                                chessgame.board[7][4] = 0
                            elif x == 7 and y == 6 and b1 and c1:
                                castling = 1
                                chessgame.board[7][4] = 0
                                chessgame.board[7][7] = 0
                                chessgame.board[7][6] = 100
                                chessgame.board[7][5] = 7
                            else:
                                chessgame.board[x][y] = chessgame.board[a][b]
                                chessgame.board[a][b] = 0
                        else:
                            a1, b1, c1 = chessgame.castleRightsWhite
                            if x == 0 and y == 2 and a1 and b1:
                                castling = 1
                                chessgame.board[0][2] = 100
                                chessgame.board[0][3] = 7
                                chessgame.board[0][0] = 0
                                chessgame.board[0][1] = 0
                                chessgame.board[0][4] = 0
                            elif x == 7 and y == 6 and b1 and c1:
                                castling = 1
                                chessgame.board[0][4] = 0
                                chessgame.board[0][7] = 0
                                chessgame.board[0][6] = 100
                                chessgame.board[0][5] = 7
                            else:
                                chessgame.board[x][y] = chessgame.board[a][b]
                                chessgame.board[a][b] = 0
                    if chessgame.board in legalMoves:
                        if castling:
                            chessgame.castleRightsWhite = [0, 0, 0]
                            castling = 0
                        chessgame.whiteMove = not chessgame.whiteMove
                        chessgame.basicChecks()
                        squareSelect = ()
                        squareClick = []
                    else:
                        squareSelect = ()
                        squareClick = []
                        chessgame.board = copy.deepcopy(revert)
    else:
        # Check for Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                row = loc[0] // 64
                col = loc[1] // 64
                if col == 8:
                    print("\nDEBUG LOG\n----------\n")
                    chessgame.debug()
                    continue
    fromX, fromY = chessgame.botFrom
    screen.blit(chessboard, (0, 0))
    screen.blit(render("Debug", pygame.font.SysFont('Times New Roman', 50)), (185, 512))
    for i in range(8):
        for j in range(8):
            piece = chessgame.board[i][j]
            todo = None
            if piece == -7:
                todo = bR
            elif piece == -3:
                todo = bN
            elif piece == -4:
                todo = bB
            elif piece == -10:
                todo = bQ
            elif piece == -100:
                todo = bK
            elif piece == -1:
                todo = bP
            elif piece == 7:
                todo = wR
            elif piece == 3:
                todo = wN
            elif piece == 4:
                todo = wB
            elif piece == 10:
                todo = wQ
            elif piece == 100:
                todo = wK
            elif piece == 1:
                todo = wP
            else:
                continue
            screen.blit(todo, (64 * j, 64 * i))
    if not chessgame.gameOver:
        if len(squareClick) == 1:
            a, b = squareClick[0]
            screen.blit(frame, (64 * a - 1, 64 * b))
        screen.blit(frame2, (64 * fromY - 1, 64 * fromX))
    else:
        if chessgame.gameResult == 0:
            screen.blit(render("Stalemate", font), (115, 214))
        elif chessgame.gameResult == 1:
            screen.blit(render("White Wins", font), (90, 214))
        else:
            screen.blit(render("Black Wins", font), (100, 214))
    pygame.display.flip()
    if not chessgame.gameOver:
        # Chess engine's turn
        if players == 0:
            if chessgame.whiteMove:
                chessgame.makeMoveMinimax()
                chessgame.basicChecks()
            else:
                chessgame.makeMoveMinimax()
                chessgame.basicChecks()
        elif playingWhite != chessgame.whiteMove and players == 1:
            # Chess engine turn
            chessgame.makeMoveMinimax()
            chessgame.basicChecks()
    if players == 0:
        time.sleep(0.5)


# Quit Pygame
pygame.quit()