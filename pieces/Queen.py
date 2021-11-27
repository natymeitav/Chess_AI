from Piece import Piece
import numpy as np

class Queen(Piece):
    def __init__(self,isWhite,pos, serial):
        Piece.__init__(self,isWhite,pos,"Q", serial)
        self.value = 90 + 180 * (self.isWhite - 1)

    # check if queen can perform move
    def canMakeMove(self, new, logicBoard):
        if self.pos[0] == new[0] and self.pos[1] < new[1]:  # right to new position
            return np.all(logicBoard[self.pos[0], self.pos[1] + 1:new[1]] == None)

        elif self.pos[0] == new[0] and self.pos[1] > new[1]:  # left to new position
            return np.all(logicBoard[self.pos[0], new[1] + 1:self.pos[1]] == None)

        elif self.pos[0] < new[0] and self.pos[1] == new[1]:  # under new position
            return np.all(logicBoard[self.pos[0] + 1:new[0], self.pos[1]] == None)

        elif self.pos[0] > new[0] and self.pos[1] == new[1]:  # over new position

            return np.all(logicBoard[new[0] + 1:self.pos[0], self.pos[1]] == None)
        elif self.pos[0] - self.pos[1] == new[0] - new[1]:  # top --> bottom
            if self.pos[0] < new[0]:
                logicBoard = logicBoard[self.pos[0]:new[0] + 1, new[1]:self.pos[1] + 1]
            else:
                logicBoard = logicBoard[new[0]:self.pos[0] + 1, new[1]:self.pos[1] + 1]

            line = logicBoard.diagonal()
            return np.all(line[1:-1] == None)


        elif self.pos[0] + self.pos[1] == new[0] + new[1]:  # bottom --> top
            if self.pos[0] < new[0]:
                logicBoard = logicBoard[self.pos[0]:new[0] + 1, self.pos[1]:new[1] + 1]
            else:
                logicBoard = logicBoard[new[0]:self.pos[0] + 1, self.pos[1]:new[1] + 1]

            line = np.diagonal(np.fliplr(logicBoard))
            return np.all(line[1:-1] == None)

        return False

    # returns all potential positions
    def getMoves(self, logicBoard):
        diagonals = self.getMovesDiag(logicBoard, 1) + self.getMovesDiag(logicBoard, -1)
        lines = self.getMovesLine(logicBoard, 0) + self.getMovesLine(logicBoard, -1)
        return diagonals + lines

    # returns the potential moves on diagonal by direction (1 --> main -1 --> secondary)
    def getMovesDiag(self, logicBoard, direction):
        moves = []

        # moves over bishop
        row = self.pos[0] - 1
        col = self.pos[1] - direction

        while (-1 < row < 8 and -1 < col < 8) and logicBoard[row, col] is None:
            moves.append((row, col))
            row -= 1
            col -= direction

        if -1 < row < 8 and -1 < col < 8:
            if logicBoard[row, col].isWhite != self.isWhite:
                moves.append((row, col))

        # moves under bishop
        row = self.pos[0] + 1
        col = self.pos[1] + direction

        while (-1 < row < 8 and -1 < col < 8) and logicBoard[row, col] is None:
            moves.append((row, col))
            row += 1
            col += direction

        if -1 < row < 8 and -1 < col < 8:
            if logicBoard[row, col].isWhite != self.isWhite:
                moves.append((row, col))

        return moves

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