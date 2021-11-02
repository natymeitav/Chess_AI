from Piece import Piece


class Pawn(Piece):
    def __init__(self, isWhite, pos):
        Piece.__init__(self, isWhite, pos, "P")
        self.value = 10 + 20 * (self.isWhite - 1)

    # check if pawn can perform move
    def canMakeMove(self, new, logicBoard):
        print(self.value)
        if self.isWhite:
            coefficient = -1  # corrects for white
        else:
            coefficient = 1
        if self.firstMove and coefficient * (new[0] - self.pos[0]) == 2 and new[1] == self.pos[1]:
            if logicBoard[self.pos[0] + coefficient, self.pos[1]] is None and logicBoard[new[0], new[1]] is None:
                return True
        # forward
        if coefficient * (new[0] - self.pos[0]) == 1 and new[1] == self.pos[1] and logicBoard[new[0], new[1]] is None:
            return True
        # side capture
        elif coefficient * (new[0] - self.pos[0]) == 1 and abs(new[1] - self.pos[1]) == 1 and logicBoard[
            new[0], new[1]] is not None:
            return True
        return False

        # returns all potential positions
        def getMoves(self, logicBoard):
            return []
