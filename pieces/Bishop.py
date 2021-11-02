import numpy as np

from Piece import Piece


class Bishop(Piece):
    def __init__(self, isWhite, pos):
        Piece.__init__(self, isWhite, pos, "B")
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
        return self.getMovesLine(logicBoard) + self.getMovesLine(np.fliplr(logicBoard))

    def getMovesLine(self, logicBoard):
        moves = []

        # moves over bishop
        row = self.pos[0]-1
        col = self.pos[1]-1

        while (-1 < row < 8 and -1 < col < 8) and logicBoard[row,col] is not None:
            moves.append((row,col))
            row = row - 1
            col = col - 1

        # moves under bishop
        row = self.pos[0] + 1
        col = self.pos[1] + 1

        while (-1 < row < 8 and -1 < col < 8) and logicBoard[row,col] is not None:
            moves.append((row,col))
            row = row + 1
            col = col + 1

        return moves




