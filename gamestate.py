import copy
import random
import repertoire
import time

attack = {
    100: [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]],  # King
    10: [[0, -7], [-7, 0], [-7, -7], [7, -7], [0, -6], [-6, 0], [-6, -6], [6, -6], [0, -5], [-5, 0], [-5, -5], [5, -5], [0, -4], [-4, 0], [-4, -4], [4, -4], [0, -3], [-3, 0], [-3, -3], [3, -3], [0, -2], [-2, 0], [-2, -2], [2, -2], [0, -1], [-1, 0], [-1, -1], [1, -1], [0, 1], [1, 0], [1, 1], [-1, 1], [0, 2], [2, 0], [2, 2], [-2, 2], [0, 3], [3, 0], [3, 3], [-3, 3], [0, 4], [4, 0], [4, 4], [-4, 4], [0, 5], [5, 0], [5, 5], [-5, 5], [0, 6], [6, 0], [6, 6], [-6, 6], [0, 7], [7, 0], [7, 7], [-7, 7]],  # Queen
    7: [[0, -7], [-7, 0], [0, -6], [-6, 0], [0, -5], [-5, 0], [0, -4], [-4, 0], [0, -3], [-3, 0], [0, -2], [-2, 0], [0, -1], [-1, 0], [0, 1], [1, 0], [0, 2], [2, 0], [0, 3], [3, 0], [0, 4], [4, 0], [0, 5], [5, 0], [0, 6], [6, 0], [0, 7], [7, 0]], # Rook
    4: [[-7, -7], [7, -7], [-6, -6], [6, -6], [-5, -5], [5, -5], [-4, -4], [4, -4], [-3, -3], [3, -3], [-2, -2], [2, -2], [-1, -1], [1, -1], [1, 1], [-1, 1], [2, 2], [-2, 2], [3, 3], [-3, 3], [4, 4], [-4, 4], [5, 5], [-5, 5], [6, 6], [-6, 6], [7, 7], [-7, 7]],  # Bishop
    3: [[2, 1], [2, -1], [1, -2], [1, 2], [-2, 1], [-2, -1], [-1, -2], [-1, 2]],  # Knight
    1: [[-1, -1], [-1, 1]],  # Pawn
    -100: [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]],  # King
    -10: [[0, -7], [-7, 0], [-7, -7], [7, -7], [0, -6], [-6, 0], [-6, -6], [6, -6], [0, -5], [-5, 0], [-5, -5], [5, -5], [0, -4], [-4, 0], [-4, -4], [4, -4], [0, -3], [-3, 0], [-3, -3], [3, -3], [0, -2], [-2, 0], [-2, -2], [2, -2], [0, -1], [-1, 0], [-1, -1], [1, -1], [0, 1], [1, 0], [1, 1], [-1, 1], [0, 2], [2, 0], [2, 2], [-2, 2], [0, 3], [3, 0], [3, 3], [-3, 3], [0, 4], [4, 0], [4, 4], [-4, 4], [0, 5], [5, 0], [5, 5], [-5, 5], [0, 6], [6, 0], [6, 6], [-6, 6], [0, 7], [7, 0], [7, 7], [-7, 7]],  # Queen
    -7: [[0, -7], [-7, 0], [0, -6], [-6, 0], [0, -5], [-5, 0], [0, -4], [-4, 0], [0, -3], [-3, 0], [0, -2], [-2, 0], [0, -1], [-1, 0], [0, 1], [1, 0], [0, 2], [2, 0], [0, 3], [3, 0], [0, 4], [4, 0], [0, 5], [5, 0], [0, 6], [6, 0], [0, 7], [7, 0]], # Rook
    -4: [[-7, -7], [7, -7], [-6, -6], [6, -6], [-5, -5], [5, -5], [-4, -4], [4, -4], [-3, -3], [3, -3], [-2, -2], [2, -2], [-1, -1], [1, -1], [1, 1], [-1, 1], [2, 2], [-2, 2], [3, 3], [-3, 3], [4, 4], [-4, 4], [5, 5], [-5, 5], [6, 6], [-6, 6], [7, 7], [-7, 7]],  # Bishop
    -3: [[2, 1], [2, -1], [1, -2], [1, 2], [-2, 1], [-2, -1], [-1, -2], [-1, 2]],  # Knight
    -1: [[1, -1], [1, 1]],  # Pawn
    0: []
}

move = {
    100: [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]],  # King
    10: [[0, -7], [-7, 0], [-7, -7], [7, -7], [0, -6], [-6, 0], [-6, -6], [6, -6], [0, -5], [-5, 0], [-5, -5], [5, -5], [0, -4], [-4, 0], [-4, -4], [4, -4], [0, -3], [-3, 0], [-3, -3], [3, -3], [0, -2], [-2, 0], [-2, -2], [2, -2], [0, -1], [-1, 0], [-1, -1], [1, -1], [0, 1], [1, 0], [1, 1], [-1, 1], [0, 2], [2, 0], [2, 2], [-2, 2], [0, 3], [3, 0], [3, 3], [-3, 3], [0, 4], [4, 0], [4, 4], [-4, 4], [0, 5], [5, 0], [5, 5], [-5, 5], [0, 6], [6, 0], [6, 6], [-6, 6], [0, 7], [7, 0], [7, 7], [-7, 7]],  # Queen
    7: [[0, -7], [-7, 0], [0, -6], [-6, 0], [0, -5], [-5, 0], [0, -4], [-4, 0], [0, -3], [-3, 0], [0, -2], [-2, 0], [0, -1], [-1, 0], [0, 1], [1, 0], [0, 2], [2, 0], [0, 3], [3, 0], [0, 4], [4, 0], [0, 5], [5, 0], [0, 6], [6, 0], [0, 7], [7, 0]], # Rook
    4: [[-7, -7], [7, -7], [-6, -6], [6, -6], [-5, -5], [5, -5], [-4, -4], [4, -4], [-3, -3], [3, -3], [-2, -2], [2, -2], [-1, -1], [1, -1], [1, 1], [-1, 1], [2, 2], [-2, 2], [3, 3], [-3, 3], [4, 4], [-4, 4], [5, 5], [-5, 5], [6, 6], [-6, 6], [7, 7], [-7, 7]],  # Bishop
    3: [[2, 1], [2, -1], [1, -2], [1, 2], [-2, 1], [-2, -1], [-1, -2], [-1, 2]],  # Knight
    1: [[-1, 0]],  # Pawn
    -100: [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]],  # King
    -10: [[0, -7], [-7, 0], [-7, -7], [7, -7], [0, -6], [-6, 0], [-6, -6], [6, -6], [0, -5], [-5, 0], [-5, -5], [5, -5], [0, -4], [-4, 0], [-4, -4], [4, -4], [0, -3], [-3, 0], [-3, -3], [3, -3], [0, -2], [-2, 0], [-2, -2], [2, -2], [0, -1], [-1, 0], [-1, -1], [1, -1], [0, 1], [1, 0], [1, 1], [-1, 1], [0, 2], [2, 0], [2, 2], [-2, 2], [0, 3], [3, 0], [3, 3], [-3, 3], [0, 4], [4, 0], [4, 4], [-4, 4], [0, 5], [5, 0], [5, 5], [-5, 5], [0, 6], [6, 0], [6, 6], [-6, 6], [0, 7], [7, 0], [7, 7], [-7, 7]],  # Queen
    -7: [[0, -7], [-7, 0], [0, -6], [-6, 0], [0, -5], [-5, 0], [0, -4], [-4, 0], [0, -3], [-3, 0], [0, -2], [-2, 0], [0, -1], [-1, 0], [0, 1], [1, 0], [0, 2], [2, 0], [0, 3], [3, 0], [0, 4], [4, 0], [0, 5], [5, 0], [0, 6], [6, 0], [0, 7], [7, 0]], # Rook
    -4: [[-7, -7], [7, -7], [-6, -6], [6, -6], [-5, -5], [5, -5], [-4, -4], [4, -4], [-3, -3], [3, -3], [-2, -2], [2, -2], [-1, -1], [1, -1], [1, 1], [-1, 1], [2, 2], [-2, 2], [3, 3], [-3, 3], [4, 4], [-4, 4], [5, 5], [-5, 5], [6, 6], [-6, 6], [7, 7], [-7, 7]],  # Bishop
    -3: [[2, 1], [2, -1], [1, -2], [1, 2], [-2, 1], [-2, -1], [-1, -2], [-1, 2]],  # Knight
    -1: [[1, 0]],  # Pawn
    0: []
}

cache = {}
legalMoves = {}
dp = {}
checkCache = {}

# Piece Table Taken from
# https://www.chessprogramming.org/Simplified_Evaluation_Function

actualValue = {
    1: 100,
    3: 280,
    4: 320,
    7: 512,
    10: 929,
    100: 6000
}

score = {
    1: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [78, 83, 86, 73, 102, 82, 85, 90],
        [7, 29, 21, 44, 40, 31, 44, 7],
        [-17, 16, -2, 15, 14, 0, 15, -13],
        [-26, 3, 10, 9, 6, 1, 0, -23],
        [-22, 9, 5, -11, -10, -2, 3, -19],
        [-31, 8, -7, -37, -36, -14, 3, -31],
        [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
    ],
    3: [
        [-66, -53, -75, -75, -10, -55, -58, -70],
        [-3, -6, 100, -36, 4, 62, -4, -14],
        [10, 67, 1, 74, 73, 27, 62, -2],
        [24, 24, 45, 37, 33, 41, 25, 17],
        [-1, 5, 31, 21, 22, 35, 2, 0],
        [-18, 10, 13, 22, 18, 15, 11, -14],
        [-23, -15, 2, 0, 2, 0, -23, -20],
        [-66, -53, -75, -75, -10, -55, -58, -70]
    ],
    4: [
        [-59, -78, -82, -76, -23, -107, -37, -50],
        [-11, 20, 35, -42, -39, 31, 2, -22],
        [-9, 39, -32, 41, 52, -10, 28, -14],
        [25, 17, 20, 34, 26, 25, 15, 10],
        [13, 10, 17, 23, 17, 16, 0, 7],
        [14, 25, 24, 15, 8, 25, 20, 15],
        [19, 20, 11, 6, 7, 6, 20, 16],
        [-7, 2, -15, -12, -14, -15, -10, -10]
    ],
    7: [
        [35, 29, 33, 4, 37, 33, 56, 50],
        [55, 29, 56, 67, 55, 62, 34, 60],
        [19, 35, 28, 33, 45, 27, 25, 15],
        [0, 5, 16, 13, 18, -4, -9, -6],
        [-28, -35, -16, -21, -13, -29, -46, -30],
        [-42, -28, -42, -25, -25, -35, -26, -46],
        [-53, -38, -31, -26, -29, -43, -44, -53],
        [-30, -24, -18, 0, -2, 0, -31, -32]
    ],
    10: [
        [6, 1, -8, -104, 69, 24, 88, 26],
        [14, 32, 60, -10, 20, 76, 57, 24],
        [-2, 43, 32, 60, 72, 63, 43, 2],
        [1, -16, 22, 17, 25, 20, -13, -6],
        [-14, -15, -2, -5, -1, -10, -20, -22],
        [-30, -6, -13, -11, -16, -11, -16, -27],
        [-36, -18, 0, -19, -15, -15, -21, -38],
        [-39, -30, -31, -13, -31, -36, -34, -42]
    ],
    100: [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 30, 0, 0, 0, 30, 0]
    ],
}

DEPTH = 3


class Game:
    def __init__(self, startPos):
        # board information:
        # 1: pawn; 3: knight; 4: bishop; 7: rook; 10: queen; 100: king
        # top: black (-), bottom: white (+)
        self.board = startPos
        self.whiteMove = True
        self.botFrom = [-1, -1]
        self.castleRightsWhite = [1, 1, 1]
        self.castleRightsBlack = [1, 1, 1]
        self.seen = {}
        self.gameOver = False
        self.gameResult = 0

    def debug(self):
        print(f'Current Board: {self.board}')
        print(f'Board Score: {self.evaluate(self.board)}')
        print(f'White to move: {self.whiteMove}')
        print(f'White castling rights: {self.castleRightsWhite}, Black castling rights: {self.castleRightsBlack}')
        print(f'Is in check: {self.inCheck()}')
        # print(f'Board has been seen {self.seen[self.hash()]} times')
        print(f'Game end state: {self.gameEnd()}')
        print(f'Possible moves: {len(self.generateMoves())}')
        print(self.generateMoves())

    def basicChecks(self):
        if self.hash() in self.seen:
            self.seen[self.hash()] += 1
            if self.seen[self.hash()] >= 3:
                self.gameOver = True
                print("Stalemate")
        else:
            self.seen[self.hash()] = 1
        if len(self.generateMoves()) == 0:
            if self.inCheck():
                if self.whiteMove == 1:
                    self.gameOver = True
                    self.gameResult = -1
                    print("Black Wins from Checkmate")
                else:
                    self.gameOver = True
                    self.gameResult = 1
                    print("White Wins from Checkmate")
            else:
                self.gameOver = True
                print("Stalemate")
        if self.board[7][0] != 7:
            a, b, c = self.castleRightsWhite
            self.castleRightsWhite = [0, b, c]
        if self.board[7][7] != 7:
            a, b, c = self.castleRightsWhite
            self.castleRightsWhite = [a, b, 0]
        if self.board[7][4] != 100:
            a, b, c = self.castleRightsWhite
            self.castleRightsWhite = [0, 0, 0]
        if self.board[0][0] != -7:
            a, b, c = self.castleRightsBlack
            self.castleRightsBlack = [0, b, c]
        if self.board[0][4] != -100:
            a, b, c = self.castleRightsBlack
            self.castleRightsBlack = [0, 0, 0]
        if self.board[0][7] != -7:
            a, b, c = self.castleRightsBlack
            self.castleRightsBlack = [a, b, 0]

    def hash(self):
        return str(self.board) + str(self.whiteMove) + str(self.castleRightsWhite) + str(self.castleRightsBlack)

    def generateMoves(self):
        validMoves = []
        if self.hash() in legalMoves:
            return legalMoves[self.hash()]
        revert = copy.deepcopy(self.board)
        # Check for castling
        if not self.inCheck():
            if self.whiteMove == 1:
                a, b, c = self.castleRightsWhite
                # Queen side castle
                if a == 1 and b == 1:
                    if self.board[7][1] == 0 and self.board[7][2] == 0 and self.board[7][3] == 0:
                        if not self.inCheck(7, 2) and not self.inCheck(7, 3):
                            self.board[7][0] = 0
                            self.board[7][2] = 100
                            self.board[7][3] = 7
                            self.board[7][4] = 0
                            validMoves.append(copy.deepcopy(self.board))
                            self.board = copy.deepcopy(revert)
                # King side castle
                if b == 1 and c == 1:
                    if self.board[7][5] == 0 and self.board[7][6] == 0:
                        if not self.inCheck(7, 5) and not self.inCheck(7, 6):
                            self.board[7][4] = 0
                            self.board[7][5] = 7
                            self.board[7][6] = 100
                            self.board[7][7] = 0
                            validMoves.append(copy.deepcopy(self.board))
                            self.board = copy.deepcopy(revert)
            else:
                a, b, c = self.castleRightsBlack
                # Queen side castle
                if a == 1 and b == 1:
                    if self.board[0][1] == 0 and self.board[0][2] == 0 and self.board[0][3] == 0:
                        if not self.inCheck(0, 2) and not self.inCheck(0, 3):
                            self.board[0][0] = 0
                            self.board[0][2] = -100
                            self.board[0][3] = -7
                            self.board[0][4] = 0
                            validMoves.append(copy.deepcopy(self.board))
                            self.board = copy.deepcopy(revert)
                # King side castle
                if b == 1 and c == 1:
                    if self.board[0][4] == -100 and self.board[0][5] == 0:
                        if not self.inCheck(0, 5) and not self.inCheck(0, 6):
                            self.board[0][4] = 0
                            self.board[0][5] = -7
                            self.board[0][6] = -100
                            self.board[0][7] = 0
                            validMoves.append(copy.deepcopy(self.board))
                            self.board = copy.deepcopy(revert)
        # Loop through all pieces
        for i in range(8):
            for j in range(8):
                if self.whiteMove and self.board[i][j] >= 1:

                    if self.board[i][j] == 1:
                        # move forwards
                        if i == 6:
                            # move forwards by 2
                            if self.board[5][j] == 0 and self.board[4][j] == 0:
                                self.board[4][j] = self.board[6][j]
                                self.board[6][j] = 0
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)
                        if self.board[i-1][j] == 0:
                            # move forwards by 1
                            self.board[i-1][j] = self.board[i][j]
                            self.board[i][j] = 0
                            if i == 1:
                                self.board[i-1][j] = 10
                            if not self.inCheck():
                                validMoves.append(copy.deepcopy(self.board))
                            self.board = copy.deepcopy(revert)
                        # take
                        if valid(i-1, j-1):
                            if self.board[i-1][j-1] < 0:
                                self.board[i-1][j-1] = self.board[i][j]
                                self.board[i][j] = 0
                                if i == 1:
                                    self.board[i-1][j-1] = 10
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)
                        if valid(i-1, j+1):
                            if self.board[i-1][j+1] < 0:
                                self.board[i-1][j+1] = self.board[i][j]
                                self.board[i][j] = 0
                                if i == 1:
                                    self.board[i-1][j+1] = 10
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)

                    if self.board[i][j] == 3:
                        for a, b in move[3]:
                            x = a + i
                            y = b + j
                            if not valid(x, y):
                                continue
                            if self.board[x][y] <= 0:
                                self.board[x][y] = self.board[i][j]
                                self.board[i][j] = 0
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)

                    if self.board[i][j] == 4 or self.board[i][j] == 10:
                        # Queen or Bishop
                        m = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
                        for a, b in m:
                            for k in range(1, 8):
                                x = i + k * a
                                y = j + k * b
                                if not valid(x, y):
                                    break
                                elif self.board[x][y] > 0:
                                    break
                                else:
                                    self.board[x][y] = self.board[i][j]
                                    self.board[i][j] = 0
                                    if not self.inCheck():
                                        validMoves.append(copy.deepcopy(self.board))
                                    self.board = copy.deepcopy(revert)
                                    if self.board[x][y] < 0:
                                        break

                    if self.board[i][j] == 7 or self.board[i][j] == 10:
                        # Queen or Rook
                        m1 = [(0, -1), (0, 1), (1, 0), (-1, 0)]
                        for a, b in m1:
                            for k in range(1, 8):
                                x = i + k * a
                                y = j + k * b
                                if not valid(x, y):
                                    break
                                elif self.board[x][y] > 0:
                                    break
                                else:
                                    self.board[x][y] = self.board[i][j]
                                    self.board[i][j] = 0
                                    if not self.inCheck():
                                        validMoves.append(copy.deepcopy(self.board))
                                    self.board = copy.deepcopy(revert)
                                    if self.board[x][y] < 0:
                                        break

                    if self.board[i][j] == 100:
                        for a, b in move[100]:
                            x = a + i
                            y = b + j
                            if not valid(x, y):
                                continue
                            if self.board[x][y] <= 0:
                                self.board[x][y] = self.board[i][j]
                                self.board[i][j] = 0
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)

                elif not self.whiteMove and self.board[i][j] <= -1:
                    if self.board[i][j] == -1:
                        if i == 1:
                            # move forwards by 2
                            if self.board[2][j] == 0 and self.board[3][j] == 0:
                                self.board[3][j] = self.board[1][j]
                                self.board[1][j] = 0
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)
                        if self.board[i + 1][j] == 0:
                            # move forwards by 1
                            self.board[i + 1][j] = self.board[i][j]
                            self.board[i][j] = 0
                            if i == 6:
                                self.board[7][j] = -10
                            if not self.inCheck():
                                validMoves.append(copy.deepcopy(self.board))
                            self.board = copy.deepcopy(revert)
                        # take
                        if valid(i+1, j-1):
                            if self.board[i + 1][j - 1] > 0:
                                self.board[i + 1][j - 1] = self.board[i][j]
                                self.board[i][j] = 0
                                if i == 6:
                                    self.board[i + 1][j-1] = -10
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)
                        if valid(i+1, j+1):
                            if self.board[i + 1][j + 1] > 0:
                                self.board[i + 1][j + 1] = self.board[i][j]
                                self.board[i][j] = 0
                                if i == 6:
                                    self.board[i + 1][j+1] = -10
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)

                    if self.board[i][j] == -3:
                        for a, b in move[-3]:
                            x = a + i
                            y = b + j
                            if not valid(x, y):
                                continue
                            if self.board[x][y] >= 0:
                                self.board[x][y] = self.board[i][j]
                                self.board[i][j] = 0
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)

                    if self.board[i][j] == -4 or self.board[i][j] == -10:
                        # Queen or Bishop
                        m = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
                        for a, b in m:
                            for k in range(1, 8):
                                x = i + k * a
                                y = j + k * b
                                if not valid(x, y):
                                    break
                                elif self.board[x][y] < 0:
                                    break
                                else:
                                    self.board[x][y] = self.board[i][j]
                                    self.board[i][j] = 0
                                    if not self.inCheck():
                                        validMoves.append(copy.deepcopy(self.board))
                                    self.board = copy.deepcopy(revert)
                                    if self.board[x][y] > 0:
                                        break

                    if self.board[i][j] == -7 or self.board[i][j] == -10:
                        # Queen or Rook
                        m1 = [(0, -1), (0, 1), (1, 0), (-1, 0)]
                        for a, b in m1:
                            for k in range(1, 8):
                                x = i + k * a
                                y = j + k * b
                                if not valid(x, y):
                                    break
                                elif self.board[x][y] < 0:
                                    break
                                else:
                                    self.board[x][y] = self.board[i][j]
                                    self.board[i][j] = 0
                                    if not self.inCheck():
                                        validMoves.append(copy.deepcopy(self.board))
                                    self.board = copy.deepcopy(revert)
                                    if self.board[x][y] > 0:
                                        break

                    if self.board[i][j] == -100:
                        for a, b in move[-100]:
                            x = a + i
                            y = b + j
                            if not valid(x, y):
                                continue
                            if self.board[x][y] >= 0:
                                self.board[x][y] = self.board[i][j]
                                self.board[i][j] = 0
                                if not self.inCheck():
                                    validMoves.append(copy.deepcopy(self.board))
                                self.board = copy.deepcopy(revert)

        if self.whiteMove == 1:
            legalMoves[self.hash()] = sorted(validMoves, key=sortScore, reverse=True)
            return legalMoves[self.hash()]
        else:
            legalMoves[self.hash()] = sorted(validMoves, key=sortScore)
            return legalMoves[self.hash()]

    def inCheck(self, checkX=-1, checkY=-1):
        kingX = 0
        kingY = 0
        if checkX == -1 and checkY == -1:
            if self.hash() in checkCache:
                return checkCache[self.hash()]
        multiplier = 1
        if self.whiteMove == 0:
            multiplier = -1
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == multiplier*100:
                    kingX = i
                    kingY = j
        if checkX != -1 and checkY != -1:
            kingX = checkX
            kingY = checkY
        # Pawn Check
        if self.whiteMove:
            if valid(kingX-1, kingY-1):
                if self.board[kingX-1][kingY-1] == -1:
                    if checkX == -1 and checkY == -1:
                        checkCache[self.hash()] = 1
                    return 1
            if valid(kingX-1, kingY+1):
                if self.board[kingX-1][kingY+1] == -1:
                    if checkX == -1 and checkY == -1:
                        checkCache[self.hash()] = 1
                    return 1
        else:
            if valid(kingX+1, kingY-1):
                if self.board[kingX+1][kingY-1] == 1:
                    if checkX == -1 and checkY == -1:
                        checkCache[self.hash()] = 1
                    return 1
            if valid(kingX+1, kingY+1):
                if self.board[kingX+1][kingY+1] == 1:
                    if checkX == -1 and checkY == -1:
                        checkCache[self.hash()] = 1
                    return 1
        # King Check
        for a, b in attack[100]:
            if valid(kingX + a, kingY + b):
                if self.board[kingX+a][kingY+b] == multiplier*-100:
                    if checkX == -1 and checkY == -1:
                        checkCache[self.hash()] = 1
                    return 1
        # Rook/Queen Check
        m = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for a, b in m:
            for i in range(1, 8):
                x = kingX + i * a
                y = kingY + i * b
                if not valid(x, y):
                    break
                if self.board[x][y] != 0:
                    if self.board[x][y] == multiplier*-7 or self.board[x][y] == multiplier*-10:
                        if checkX == -1 and checkY == -1:
                            checkCache[self.hash()] = 1
                        return 1
                    break
        # Bishop/Queen Check
        m1 = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
        for a, b in m1:
            for i in range(1, 8):
                x = kingX + i * a
                y = kingY + i * b
                if not valid(x, y):
                    break
                if self.board[x][y] != 0:
                    if self.board[x][y] == multiplier * -4 or self.board[x][y] == multiplier * -10:
                        if checkX == -1 and checkY == -1:
                            checkCache[self.hash()] = 1
                        return 1
                    break
        # Knight Check
        for a, b in attack[3]:
            if valid(kingX + a, kingY + b):
                if self.board[kingX + a][kingY + b] == multiplier*-3:
                    if checkX == -1 and checkY == -1:
                        checkCache[self.hash()] = 1
                    return 1

    def makeMoveGreedy(self):
        validMoves = self.generateMoves()
        bestPosition = copy.deepcopy(self.board)
        if self.whiteMove:
            bestScore = -1000000
            for currState in validMoves:
                currScore = self.evaluate(currState)
                if currScore > bestScore:
                    bestScore = copy.deepcopy(currScore)
                    bestPosition = copy.deepcopy(currState)
        else:
            bestScore = 1000000
            for currState in validMoves:
                currScore = self.evaluate(currState)
                if currScore < bestScore:
                    bestScore = copy.deepcopy(currScore)
                    bestPosition = copy.deepcopy(currState)
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0 and bestPosition[i][j] == 0:
                    self.botFrom = [i, j]
        self.board = bestPosition
        self.basicChecks()
        self.whiteMove = not self.whiteMove

    def makeMoveRandom(self):
        bestPosition = random.choice(self.generateMoves())
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0 and bestPosition[i][j] == 0:
                    self.botFrom = [i, j]
        self.board = bestPosition
        self.basicChecks()
        self.whiteMove = not self.whiteMove

    def makeMoveMinimax(self):
        global bestBoard
        bestBoard = [[0]]
        multiplier = 1
        if self.whiteMove:
            bookW = repertoire.whiteBookMoves
            if str(self.board) in bookW:
                self.board = copy.deepcopy(random.choice(bookW[str(self.board)]))
                self.whiteMove = not self.whiteMove
                print(self.board)
                time.sleep(0.5)
                return
        else:
            bookB = repertoire.blackBookMoves
            if str(self.board) in bookB:
                self.board = copy.deepcopy(random.choice(bookB[str(self.board)]))
                self.whiteMove = not self.whiteMove
                time.sleep(0.5)
                return
        if self.whiteMove == 0:
            multiplier = -1
        self.minimax(DEPTH, -2000000, 2000000, multiplier)
        if bestBoard != [[0]]:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] != 0 and bestBoard[i][j] == 0:
                        self.botFrom = [i, j]
            self.board = copy.deepcopy(bestBoard)
            self.whiteMove = not self.whiteMove
        else:
            print("ERROR: NO VALID BOARD STATE FOUND")

    def minimax(self, depth, alpha, beta, multiplier):
        # print(f"minimax at depth {depth}. alpha: {alpha}, beta: {beta}, multiplier = {multiplier}")
        global bestBoard
        revert = copy.deepcopy(self.board)
        validMoves = self.generateMoves()
        if len(validMoves) == 0:
            if not self.inCheck():
                return 0
            return -1000000
        if str([self.hash(), depth]) in dp and depth < DEPTH:
            return dp[str([self.hash(), depth])]
        if depth == 0 or (self.gameEnd() != 1 and abs(self.gameEnd()) != 100):
            if abs(self.gameEnd() * multiplier) == 1000000:
                return 1000000
            return multiplier * self.evaluate(self.board)
        bestScore = -2000000
        for currState in validMoves:
            self.board = copy.deepcopy(currState)
            self.whiteMove = not self.whiteMove
            currScore = -self.minimax(depth - 1, -beta, -alpha, -multiplier)
            self.whiteMove = not self.whiteMove
            self.board = copy.deepcopy(revert)
            if currScore > bestScore:
                bestScore = currScore
                if depth == DEPTH:
                    bestBoard = copy.deepcopy(currState)
            alpha = max(alpha, currScore)
            if alpha >= beta:
                break
        for i in range(1, depth+1):
            dp[str([self.hash(), i])] = bestScore
        return bestScore

    def evaluate(self, b):
        revert = copy.deepcopy(self.board)
        self.board = copy.deepcopy(b)
        self.whiteMove = not self.whiteMove
        res = self.gameEnd()
        self.whiteMove = not self.whiteMove
        if res != 1 and abs(res) != 100:
            self.board = copy.deepcopy(revert)
            return res
        if self.hash() in cache:
            temp = copy.deepcopy(self.hash())
            self.board = copy.deepcopy(revert)
            return cache[self.hash()]
        whiteScore = 0
        blackScore = 0
        whiteScore += res
        for i in range(8):
            for j in range(8):
                if self.board[i][j] > 0:
                    # White Piece
                    whiteScore += getScore(i, j, self.board)
                elif self.board[i][j] < 0:
                    # Black Piece
                    blackScore += getScore(i, j, self.board)
        self.board = copy.deepcopy(revert)
        cache[self.hash()] = whiteScore + blackScore
        return cache[self.hash()]

    def gameEnd(self):
        if len(self.generateMoves()) == 0:
            if self.inCheck():
                if self.whiteMove == 1:
                    return -1000000
                else:
                    return 1000000
            else:
                return 0
        if self.inCheck():
            if self.whiteMove:
                return -100
            else:
                return 100
        return 1


def valid(x, y):
    if 0 <= x:
        if x < 8:
            if 0 <= y:
                if y < 8:
                    return 1
    return 0


def sortScore(board):
    whiteScore = 0
    blackScore = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] > 0:
                # White Piece
                whiteScore += getScore(i, j, board)
            elif board[i][j] < 0:
                # Black Piece
                blackScore += getScore(i, j, board)
    return whiteScore + blackScore


def getScore(i, j, board):
    if board[i][j] > 0:
        return actualValue[board[i][j]] + score[board[i][j]][i][j]
    else:
        return -actualValue[-board[i][j]] - score[-board[i][j]][7-i][j]