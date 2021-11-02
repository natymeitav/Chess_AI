import numpy as np

from Piece import Piece


class Rook(Piece):
    def __init__(self, isWhite, pos):
        Piece.__init__(self, isWhite, pos, "R")
        self.value = 50 + 100 * (self.isWhite - 1)

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

    # returns all potential positions
    def getMoves(self, logicBoard):
        return []