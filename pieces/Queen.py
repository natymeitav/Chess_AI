from Piece import Piece
import numpy as np

class Queen(Piece):
    def __init__(self,isWhite,pos):
        Piece.__init__(self,isWhite,pos,"Q")
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
        return []