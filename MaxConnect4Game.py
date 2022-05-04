#!/usr/bin/env python

import copy
import random
import sys

utilityValue = {}
score_list = []
infinity = float('inf')


class MaxConnect4game:
    def __init__(self):
        self.currentGameBoard = [[0 for i in range(7)] for j in range(6)]
        self.presentMove = 0
        self.piece_count = 0
        self.depth = 1
        self.gameFile = None
        self.computer_column = None
        self.player1Score = 0
        self.player2Score = 0

    def checkPieceCount(self):
        self.piece_count = sum(1 for row in self.currentGameBoard for piece in row if piece)

    def getPieceCount(self):
        return sum(1 for row in self.currentGameBoard for piece in row if piece)

    def printcurrentGameBoard(self):
        print("............................................")
        for i in range(6):
            print("||"),
            for j in range(7):
                print('%d ' % int(self.currentGameBoard[i][j]), end=" "),
            print("||")
        print("............................................")

    def printGameBoardToFile(self):
        for row in self.currentGameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r')
        self.gameFile.write('%s\r' % str(self.presentMove))

    def minimax(self, depth):
        presentState = copy.deepcopy(self.currentGameBoard)
        for i in range(7):
            if self.playPiece(i) != None:
                if self.piece_count == 42 or self.depth == 0:
                    self.currentGameBoard = copy.deepcopy(presentState)
                    return i
                else:
                    val = self.minVal(self.currentGameBoard, -infinity, infinity, depth - 1)

                    utilityValue[i] = val
                    self.currentGameBoard = copy.deepcopy(presentState)

        maxUtilityValue = max([i for i in utilityValue.values()])
        for i in range(7):
            if i in utilityValue:
                if utilityValue[i] == maxUtilityValue:
                    utilityValue.clear()
                    return i

    def max_val(self, current_node, alpha, beta, depth):
        parent_node = copy.deepcopy(current_node)
        value = -infinity
        child_nodes = []
        for i in range(7):
            presentState = self.playPiece(i)
            if presentState != None:
                child_nodes.append(self.currentGameBoard)
                self.currentGameBoard = copy.deepcopy(parent_node)

        if child_nodes == [] or depth == 0:
            self.countScore(self.currentGameBoard)
            return self.evaluationFunction(self.currentGameBoard)
        else:
            for node in child_nodes:
                self.currentGameBoard = copy.deepcopy(node)
                value = max(value, self.minVal(node, alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

    def minVal(self, current_node, alpha, beta, depth):
        parent_node = copy.deepcopy(current_node)
        if self.presentMove == 1:
            opponent = 2
        elif self.presentMove == 2:
            opponent = 1
        value = infinity
        child_nodes = []
        for i in range(7):
            presentState = self.check_piece(i, opponent)
            if presentState != None:
                child_nodes.append(self.currentGameBoard)
                self.currentGameBoard = copy.deepcopy(parent_node)

        if child_nodes == [] or depth == 0:
            self.countScore(self.currentGameBoard)
            return self.evaluationFunction(self.currentGameBoard)
        else:
            for node in child_nodes:
                self.currentGameBoard = copy.deepcopy(node)
                value = min(value, self.max_val(node, alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
        return value

    def evaluationFunction(self, state):
        if self.presentMove == 1:
            o_color = 2
        elif self.presentMove == 2:
            o_color = 1
        self_fours = self.checkForStreak(state, self.presentMove, 4)
        self_threes = self.checkForStreak(state, self.presentMove, 3)
        self_twos = self.checkForStreak(state, self.presentMove, 2)
        Opponent_fours = self.checkForStreak(state, o_color, 4)
        Opponent_threes = self.checkForStreak(state, o_color, 3)
        Opponent_twos = self.checkForStreak(state, o_color, 2)
        selfScore = self_fours * 4 + self_threes * 3 + self_twos * 2
        opponentScore = Opponent_fours * 4 + Opponent_threes * 3 + Opponent_twos * 2
        return (selfScore) - (opponentScore)
    def aiPlay(self):
        random_column = self.minimax(int(self.depth))
        result = self.playPiece(random_column)
        if not result:
            print('No Result')
        else:
            print('Player: %d, Column: %d\n' % (self.presentMove, random_column + 1))
            self.change_move()

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.currentGameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.currentGameBoard[i][column]:
                    self.currentGameBoard[i][column] = self.presentMove
                    self.piece_count += 1
                    return 1

    def change_move(self):
        if self.presentMove == 2:
            self.presentMove = 1
        elif self.presentMove == 1:
            self.presentMove = 2

    def checkForStreak(self, state, color, streak):
        count = 0
        for m in range(6):
            for n in range(7):
                if state[m][n] != color:
                    break
                else:
                    count += self.verticalStreak(m, n, state, streak)
                    count += self.horizontalStreak(m, n, state, streak)
                    count += self.diagonalCheck(m, n, state, streak)
        return count

    def verticalStreak(self, row, column, state, streak):
        consecutiveCount = 0
        for m in range(row, 6):
            if state[m][column] != state[row][column]:
                break
            else:
                consecutiveCount += 1
        if consecutiveCount < streak:
            return 0
        else:
            return 1

    def horizontalStreak(self, row, column, state, streak):
        count = 0
        for n in range(column, 7):
            if state[row][n] != state[row][column]:
                break
            else:
                count += 1
        if count < streak:
            return 0
        else:
            return 1

    def diagonalCheck(self, row, column, state, streak):
        total = 0
        count = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        count = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        return total

    def check_piece(self, column, opponent):
        if not self.currentGameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.currentGameBoard[i][column]:
                    self.currentGameBoard[i][column] = opponent
                    self.piece_count += 1
                    return 1

    def countTotalScore(self):
        self.player1Score = 0;
        self.player2Score = 0;
        # Check horizontally
        for row in self.currentGameBoard:
            # Check player 1
            if row[0:4] == [1] * 4:
                self.player1Score += 1
            if row[1:5] == [1] * 4:
                self.player1Score += 1
            if row[2:6] == [1] * 4:
                self.player1Score += 1
            if row[3:7] == [1] * 4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2] * 4:
                self.player2Score += 1
            if row[1:5] == [2] * 4:
                self.player2Score += 1
            if row[2:6] == [2] * 4:
                self.player2Score += 1
            if row[3:7] == [2] * 4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.currentGameBoard[0][j] == 1 and self.currentGameBoard[1][j] == 1 and
                    self.currentGameBoard[2][j] == 1 and self.currentGameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.currentGameBoard[1][j] == 1 and self.currentGameBoard[2][j] == 1 and
                    self.currentGameBoard[3][j] == 1 and self.currentGameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.currentGameBoard[2][j] == 1 and self.currentGameBoard[3][j] == 1 and
                    self.currentGameBoard[4][j] == 1 and self.currentGameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.currentGameBoard[0][j] == 2 and self.currentGameBoard[1][j] == 2 and
                    self.currentGameBoard[2][j] == 2 and self.currentGameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.currentGameBoard[1][j] == 2 and self.currentGameBoard[2][j] == 2 and
                    self.currentGameBoard[3][j] == 2 and self.currentGameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.currentGameBoard[2][j] == 2 and self.currentGameBoard[3][j] == 2 and
                    self.currentGameBoard[4][j] == 2 and self.currentGameBoard[5][j] == 2):
                self.player2Score += 1
        # Check diagonally

        # Check player 1
        if (self.currentGameBoard[2][0] == 1 and self.currentGameBoard[3][1] == 1 and
                self.currentGameBoard[4][2] == 1 and self.currentGameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][0] == 1 and self.currentGameBoard[2][1] == 1 and
                self.currentGameBoard[3][2] == 1 and self.currentGameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][1] == 1 and self.currentGameBoard[3][2] == 1 and
                self.currentGameBoard[4][3] == 1 and self.currentGameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][0] == 1 and self.currentGameBoard[1][1] == 1 and
                self.currentGameBoard[2][2] == 1 and self.currentGameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][1] == 1 and self.currentGameBoard[2][2] == 1 and
                self.currentGameBoard[3][3] == 1 and self.currentGameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][2] == 1 and self.currentGameBoard[3][3] == 1 and
                self.currentGameBoard[4][4] == 1 and self.currentGameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][1] == 1 and self.currentGameBoard[1][2] == 1 and
                self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][2] == 1 and self.currentGameBoard[2][3] == 1 and
                self.currentGameBoard[3][4] == 1 and self.currentGameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][4] == 1 and
                self.currentGameBoard[4][5] == 1 and self.currentGameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][2] == 1 and self.currentGameBoard[1][3] == 1 and
                self.currentGameBoard[2][4] == 1 and self.currentGameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][3] == 1 and self.currentGameBoard[2][4] == 1 and
                self.currentGameBoard[3][5] == 1 and self.currentGameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][3] == 1 and self.currentGameBoard[1][4] == 1 and
                self.currentGameBoard[2][5] == 1 and self.currentGameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.currentGameBoard[0][3] == 1 and self.currentGameBoard[1][2] == 1 and
                self.currentGameBoard[2][1] == 1 and self.currentGameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][4] == 1 and self.currentGameBoard[1][3] == 1 and
                self.currentGameBoard[2][2] == 1 and self.currentGameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][3] == 1 and self.currentGameBoard[2][2] == 1 and
                self.currentGameBoard[3][1] == 1 and self.currentGameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][5] == 1 and self.currentGameBoard[1][4] == 1 and
                self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][4] == 1 and self.currentGameBoard[2][3] == 1 and
                self.currentGameBoard[3][2] == 1 and self.currentGameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][2] == 1 and
                self.currentGameBoard[4][1] == 1 and self.currentGameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][6] == 1 and self.currentGameBoard[1][5] == 1 and
                self.currentGameBoard[2][4] == 1 and self.currentGameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][5] == 1 and self.currentGameBoard[2][4] == 1 and
                self.currentGameBoard[3][3] == 1 and self.currentGameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][4] == 1 and self.currentGameBoard[3][3] == 1 and
                self.currentGameBoard[4][2] == 1 and self.currentGameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][6] == 1 and self.currentGameBoard[2][5] == 1 and
                self.currentGameBoard[3][4] == 1 and self.currentGameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][5] == 1 and self.currentGameBoard[3][4] == 1 and
                self.currentGameBoard[4][3] == 1 and self.currentGameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][6] == 1 and self.currentGameBoard[3][5] == 1 and
                self.currentGameBoard[4][4] == 1 and self.currentGameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.currentGameBoard[2][0] == 2 and self.currentGameBoard[3][1] == 2 and
                self.currentGameBoard[4][2] == 2 and self.currentGameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][0] == 2 and self.currentGameBoard[2][1] == 2 and
                self.currentGameBoard[3][2] == 2 and self.currentGameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][1] == 2 and self.currentGameBoard[3][2] == 2 and
                self.currentGameBoard[4][3] == 2 and self.currentGameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][0] == 2 and self.currentGameBoard[1][1] == 2 and
                self.currentGameBoard[2][2] == 2 and self.currentGameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][1] == 2 and self.currentGameBoard[2][2] == 2 and
                self.currentGameBoard[3][3] == 2 and self.currentGameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][2] == 2 and self.currentGameBoard[3][3] == 2 and
                self.currentGameBoard[4][4] == 2 and self.currentGameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][1] == 2 and self.currentGameBoard[1][2] == 2 and
                self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][2] == 2 and self.currentGameBoard[2][3] == 2 and
                self.currentGameBoard[3][4] == 2 and self.currentGameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][4] == 2 and
                self.currentGameBoard[4][5] == 2 and self.currentGameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][2] == 2 and self.currentGameBoard[1][3] == 2 and
                self.currentGameBoard[2][4] == 2 and self.currentGameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][3] == 2 and self.currentGameBoard[2][4] == 2 and
                self.currentGameBoard[3][5] == 2 and self.currentGameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][3] == 2 and self.currentGameBoard[1][4] == 2 and
                self.currentGameBoard[2][5] == 2 and self.currentGameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.currentGameBoard[0][3] == 2 and self.currentGameBoard[1][2] == 2 and
                self.currentGameBoard[2][1] == 2 and self.currentGameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][4] == 2 and self.currentGameBoard[1][3] == 2 and
                self.currentGameBoard[2][2] == 2 and self.currentGameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][3] == 2 and self.currentGameBoard[2][2] == 2 and
                self.currentGameBoard[3][1] == 2 and self.currentGameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][5] == 2 and self.currentGameBoard[1][4] == 2 and
                self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][4] == 2 and self.currentGameBoard[2][3] == 2 and
                self.currentGameBoard[3][2] == 2 and self.currentGameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][2] == 2 and
                self.currentGameBoard[4][1] == 2 and self.currentGameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][6] == 2 and self.currentGameBoard[1][5] == 2 and
                self.currentGameBoard[2][4] == 2 and self.currentGameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][5] == 2 and self.currentGameBoard[2][4] == 2 and
                self.currentGameBoard[3][3] == 2 and self.currentGameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][4] == 2 and self.currentGameBoard[3][3] == 2 and
                self.currentGameBoard[4][2] == 2 and self.currentGameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][6] == 2 and self.currentGameBoard[2][5] == 2 and
                self.currentGameBoard[3][4] == 2 and self.currentGameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][5] == 2 and self.currentGameBoard[3][4] == 2 and
                self.currentGameBoard[4][3] == 2 and self.currentGameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][6] == 2 and self.currentGameBoard[3][5] == 2 and
                self.currentGameBoard[4][4] == 2 and self.currentGameBoard[5][3] == 2):
            self.player2Score += 1

    def countScore(self, state):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in state:
            # Check player 1
            if row[0:4] == [1] * 4:
                self.player1Score += 1
            if row[1:5] == [1] * 4:
                self.player1Score += 1
            if row[2:6] == [1] * 4:
                self.player1Score += 1
            if row[3:7] == [1] * 4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2] * 4:
                self.player2Score += 1
            if row[1:5] == [2] * 4:
                self.player2Score += 1
            if row[2:6] == [2] * 4:
                self.player2Score += 1
            if row[3:7] == [2] * 4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.currentGameBoard[0][j] == 1 and self.currentGameBoard[1][j] == 1 and
                    self.currentGameBoard[2][j] == 1 and self.currentGameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.currentGameBoard[1][j] == 1 and self.currentGameBoard[2][j] == 1 and
                    self.currentGameBoard[3][j] == 1 and self.currentGameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.currentGameBoard[2][j] == 1 and self.currentGameBoard[3][j] == 1 and
                    self.currentGameBoard[4][j] == 1 and self.currentGameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.currentGameBoard[0][j] == 2 and self.currentGameBoard[1][j] == 2 and
                    self.currentGameBoard[2][j] == 2 and self.currentGameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.currentGameBoard[1][j] == 2 and self.currentGameBoard[2][j] == 2 and
                    self.currentGameBoard[3][j] == 2 and self.currentGameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.currentGameBoard[2][j] == 2 and self.currentGameBoard[3][j] == 2 and
                    self.currentGameBoard[4][j] == 2 and self.currentGameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.currentGameBoard[2][0] == 1 and self.currentGameBoard[3][1] == 1 and
                self.currentGameBoard[4][2] == 1 and self.currentGameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][0] == 1 and self.currentGameBoard[2][1] == 1 and
                self.currentGameBoard[3][2] == 1 and self.currentGameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][1] == 1 and self.currentGameBoard[3][2] == 1 and
                self.currentGameBoard[4][3] == 1 and self.currentGameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][0] == 1 and self.currentGameBoard[1][1] == 1 and
                self.currentGameBoard[2][2] == 1 and self.currentGameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][1] == 1 and self.currentGameBoard[2][2] == 1 and
                self.currentGameBoard[3][3] == 1 and self.currentGameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][2] == 1 and self.currentGameBoard[3][3] == 1 and
                self.currentGameBoard[4][4] == 1 and self.currentGameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][1] == 1 and self.currentGameBoard[1][2] == 1 and
                self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][2] == 1 and self.currentGameBoard[2][3] == 1 and
                self.currentGameBoard[3][4] == 1 and self.currentGameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][4] == 1 and
                self.currentGameBoard[4][5] == 1 and self.currentGameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][2] == 1 and self.currentGameBoard[1][3] == 1 and
                self.currentGameBoard[2][4] == 1 and self.currentGameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][3] == 1 and self.currentGameBoard[2][4] == 1 and
                self.currentGameBoard[3][5] == 1 and self.currentGameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][3] == 1 and self.currentGameBoard[1][4] == 1 and
                self.currentGameBoard[2][5] == 1 and self.currentGameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.currentGameBoard[0][3] == 1 and self.currentGameBoard[1][2] == 1 and
                self.currentGameBoard[2][1] == 1 and self.currentGameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][4] == 1 and self.currentGameBoard[1][3] == 1 and
                self.currentGameBoard[2][2] == 1 and self.currentGameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][3] == 1 and self.currentGameBoard[2][2] == 1 and
                self.currentGameBoard[3][1] == 1 and self.currentGameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][5] == 1 and self.currentGameBoard[1][4] == 1 and
                self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][4] == 1 and self.currentGameBoard[2][3] == 1 and
                self.currentGameBoard[3][2] == 1 and self.currentGameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][3] == 1 and self.currentGameBoard[3][2] == 1 and
                self.currentGameBoard[4][1] == 1 and self.currentGameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[0][6] == 1 and self.currentGameBoard[1][5] == 1 and
                self.currentGameBoard[2][4] == 1 and self.currentGameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][5] == 1 and self.currentGameBoard[2][4] == 1 and
                self.currentGameBoard[3][3] == 1 and self.currentGameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][4] == 1 and self.currentGameBoard[3][3] == 1 and
                self.currentGameBoard[4][2] == 1 and self.currentGameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[1][6] == 1 and self.currentGameBoard[2][5] == 1 and
                self.currentGameBoard[3][4] == 1 and self.currentGameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][5] == 1 and self.currentGameBoard[3][4] == 1 and
                self.currentGameBoard[4][3] == 1 and self.currentGameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.currentGameBoard[2][6] == 1 and self.currentGameBoard[3][5] == 1 and
                self.currentGameBoard[4][4] == 1 and self.currentGameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.currentGameBoard[2][0] == 2 and self.currentGameBoard[3][1] == 2 and
                self.currentGameBoard[4][2] == 2 and self.currentGameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][0] == 2 and self.currentGameBoard[2][1] == 2 and
                self.currentGameBoard[3][2] == 2 and self.currentGameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][1] == 2 and self.currentGameBoard[3][2] == 2 and
                self.currentGameBoard[4][3] == 2 and self.currentGameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][0] == 2 and self.currentGameBoard[1][1] == 2 and
                self.currentGameBoard[2][2] == 2 and self.currentGameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][1] == 2 and self.currentGameBoard[2][2] == 2 and
                self.currentGameBoard[3][3] == 2 and self.currentGameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][2] == 2 and self.currentGameBoard[3][3] == 2 and
                self.currentGameBoard[4][4] == 2 and self.currentGameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][1] == 2 and self.currentGameBoard[1][2] == 2 and
                self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][2] == 2 and self.currentGameBoard[2][3] == 2 and
                self.currentGameBoard[3][4] == 2 and self.currentGameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][4] == 2 and
                self.currentGameBoard[4][5] == 2 and self.currentGameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][2] == 2 and self.currentGameBoard[1][3] == 2 and
                self.currentGameBoard[2][4] == 2 and self.currentGameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][3] == 2 and self.currentGameBoard[2][4] == 2 and
                self.currentGameBoard[3][5] == 2 and self.currentGameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][3] == 2 and self.currentGameBoard[1][4] == 2 and
                self.currentGameBoard[2][5] == 2 and self.currentGameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.currentGameBoard[0][3] == 2 and self.currentGameBoard[1][2] == 2 and
                self.currentGameBoard[2][1] == 2 and self.currentGameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][4] == 2 and self.currentGameBoard[1][3] == 2 and
                self.currentGameBoard[2][2] == 2 and self.currentGameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][3] == 2 and self.currentGameBoard[2][2] == 2 and
                self.currentGameBoard[3][1] == 2 and self.currentGameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][5] == 2 and self.currentGameBoard[1][4] == 2 and
                self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][2] == 2):
            self.plfiayer2Score += 1
        if (self.currentGameBoard[1][4] == 2 and self.currentGameBoard[2][3] == 2 and
                self.currentGameBoard[3][2] == 2 and self.currentGameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][3] == 2 and self.currentGameBoard[3][2] == 2 and
                self.currentGameBoard[4][1] == 2 and self.currentGameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[0][6] == 2 and self.currentGameBoard[1][5] == 2 and
                self.currentGameBoard[2][4] == 2 and self.currentGameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][5] == 2 and self.currentGameBoard[2][4] == 2 and
                self.currentGameBoard[3][3] == 2 and self.currentGameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][4] == 2 and self.currentGameBoard[3][3] == 2 and
                self.currentGameBoard[4][2] == 2 and self.currentGameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[1][6] == 2 and self.currentGameBoard[2][5] == 2 and
                self.currentGameBoard[3][4] == 2 and self.currentGameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][5] == 2 and self.currentGameBoard[3][4] == 2 and
                self.currentGameBoard[4][3] == 2 and self.currentGameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.currentGameBoard[2][6] == 2 and self.currentGameBoard[3][5] == 2 and
                self.currentGameBoard[4][4] == 2 and self.currentGameBoard[5][3] == 2):
            self.player2Score += 1
