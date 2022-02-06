import numpy as np

from Piece import Piece


class Rook(Piece):
    def __init__(self, isWhite, pos, serial):
        Piece.__init__(self, isWhite, pos, "R", serial)
        self.value = 50 - 100 * (self.isWhite)

    # check if rook can perform move
    def canMakeMove(self, new, logicBoard):
        if self.pos[0] == new[0] and self.pos[1] < new[1]:  # right to new position
            self.firstMove = False
            return np.all(logicBoard[self.pos[0], self.pos[1] + 1:new[1]] == None)

        elif self.pos[0] == new[0] and self.pos[1] > new[1]:  # left to new position
            self.firstMove = False
            return np.all(logicBoard[self.pos[0], new[1] + 1:self.pos[1]] == None)

        elif self.pos[0] < new[0] and self.pos[1] == new[1]:  # under new position
            self.firstMove = False
            return np.all(logicBoard[self.pos[0] + 1:new[0], self.pos[1]] == None)

        elif self.pos[0] > new[0] and self.pos[1] == new[1]:  # over new position
            self.firstMove = False
            return np.all(logicBoard[new[0] + 1:self.pos[0], self.pos[1]] == None)

        return False

    # returns all potential moves
    def getMoves(self, logicBoard):
        return self.getMovesLine(logicBoard, 0) + self.getMovesLine(logicBoard, -1)

    # returns the potential moves on diagonal by direction (0 --> col -1 --> row)
    def getMovesLine(self, logicBoard, direction):
        moves = []
        # moves over rook
        row = self.pos[0] - direction
        col = self.pos[1] - (direction + 1)

        while (-1 < row < 8 and -1 < col < 8) and logicBoard[row, col] is None:
            moves.append((row, col))
            row -= direction
            col -= (direction + 1)

        if -1 < row < 8 and -1 < col < 8:
            if logicBoard[row, col].isWhite != self.isWhite:
                moves.append((row, col))

        # moves under rook
        row = self.pos[0] + direction
        col = self.pos[1] + (direction + 1)

        while (-1 < row < 8 and -1 < col < 8) and logicBoard[row, col] is None:
            moves.append((row, col))
            row += direction
            col += (direction + 1)

        if -1 < row < 8 and -1 < col < 8:
            if logicBoard[row, col].isWhite != self.isWhite:
                moves.append((row, col))

        return moves
