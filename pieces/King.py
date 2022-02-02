import numpy as np

from Piece import Piece


class King(Piece):
    def __init__(self, isWhite, pos, serial):
        Piece.__init__(self, isWhite, pos, "K", serial)
        self.value = 999 + 1998 * (self.isWhite - 1)

    # check if king can perform move
    def canMakeMove(self, new, logicBoard):
        if self.can_castle(new, logicBoard):
            return True
        return abs(new[0] - self.pos[0]) <= 1 and abs(new[1] - self.pos[1]) <= 1

    def can_castle(self, new, logic):
        if (new[0] == 7 or new[0] == 0) and (new[1] == 1 or new[1] == 6):
            if new[1] == 1:
                rook_pos = [new[0], 0]
            else:
                rook_pos = [new[0], 7]
            if logic[new[0], new[1]] is None:
                if logic[rook_pos[0], rook_pos[1]] is not None:  # check if rook is in place
                    if logic[rook_pos[0], rook_pos[1]].firstMove and self.firstMove:  # check if rook and king didn't move
                        # check if path clear
                        if rook_pos[1] > new[1]:
                            return logic[new[0],5] is None
                        else:
                            return logic[new[0], 3] is None and logic[new[0], 2] is None
        return False

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

        if self.can_castle([self.pos[0],1],logicBoard):
            moves.append([self.pos[0],1])
        if self.can_castle([self.pos[0],6],logicBoard):
            moves.append([self.pos[0],1])

        return moves

    def isThreatened(self, hostiles, logic):
        for piece in hostiles:
            if piece is not None:
                if self.pos in piece.getMoves(logic):
                    return True
        return False
