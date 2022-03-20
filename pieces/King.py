import numpy as np

from Piece import Piece


class King(Piece):
    def __init__(self, isWhite, pos, serial):
        Piece.__init__(self, isWhite, pos, "K", serial)
        self.value = 900 - 1800 * (self.isWhite)

    # check if king can perform move
    def canMakeMove(self, new, logicBoard):
        if self.canCastle(new, logicBoard):
            return True
        return abs(new[0] - self.pos[0]) <= 1 and abs(new[1] - self.pos[1]) <= 1

    # returns all potential moves
    def getMoves(self, logicBoard):
        moves = []

        for row in range(self.pos[0] - 1, self.pos[0] + 2):
            for col in range(self.pos[1] - 1, self.pos[1] + 2):
                if -1 < row < 8 and -1 < col < 8:  # position is on board
                    if row != self.pos[0] or col != self.pos[1]:  # king isn't at position already
                        if logicBoard[row, col] is None:
                            moves.append((row, col))
                        elif logicBoard[row, col].isWhite != self.isWhite:
                            moves.append((row, col))

        # castling
        if self.canCastle([self.pos[0],2],logicBoard):
            moves.append([self.pos[0],2])
        if self.canCastle([self.pos[0],6],logicBoard):
            moves.append([self.pos[0],6])

        return moves

    # checks if king can castle
    def canCastle(self,new, logic):
        if self.firstMove:
            if new[1] == 2:
                rook = logic[self.pos[0],0]
                if rook is not None:
                    if rook.firstMove:
                        return np.all(logic[self.pos[0], rook.pos[1] + 1:self.pos[1]] == None)

            if new[1] == 6:
                rook = logic[self.pos[0],7]
                if rook is not None:
                    if rook.firstMove:
                        return np.all(logic[self.pos[0], self.pos[1] + 1:rook.pos[1]] == None)
