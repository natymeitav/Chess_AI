from Piece import Piece


class King(Piece):
    def __init__(self, isWhite, pos, serial):
        Piece.__init__(self, isWhite, pos, "K",serial)
        self.value = 999 + 1998 * (self.isWhite - 1)

    # check if king can perform move
    def canMakeMove(self, new, logicBoard):
        if self.firstMove:
            self.firstMove = False
        return abs(new[0] - self.pos[0]) <= 1 and abs(new[1] - self.pos[1]) <= 1

    # returns all potential moves
    def getMoves(self, logicBoard):
        moves = []

        for row in range(self.pos[0] - 1, self.pos[0] + 2):
            for col in range(self.pos[1] - 1, self.pos[1] + 2):
                if -1 < row < 8 and -1 < col < 8: # position is on board
                    if row != self.pos[0] or col != self.pos[1]: # king isn't at position already
                        if logicBoard[row,col] is None:
                            moves.append((row,col))
                        elif logicBoard[row,col].isWhite != self.isWhite:
                            moves.append((row, col))

        return moves
