import numpy as np

from Piece import Piece


class Bishop(Piece):
    def __init__(self, isWhite, pos,serial):
        Piece.__init__(self, isWhite, pos, "B",serial)
        self.value = 40 + 80 * (self.isWhite - 1)

    # check if bishop can perform move
    def canMakeMove(self, new, logicBoard):

        if self.pos[0] - self.pos[1] == new[0] - new[1]:  # top --> bottom
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

    # returns all potential moves
    def getMoves(self, logicBoard):
        return self.getMovesDiag(logicBoard, 1) + self.getMovesDiag(logicBoard, -1)

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

