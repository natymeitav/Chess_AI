from Piece import Piece


class Knight(Piece):
    def __init__(self, isWhite, pos, serial):
        self.init__ = Piece.__init__(self, isWhite, pos, "N", serial)
        self.value = 30 + 60 * (self.isWhite - 1)

    # check if knight can perform move
    def canMakeMove(self, new, logicBoard):
        return (abs(self.pos[0] - new[0]) == 1 and abs(self.pos[1] - new[1]) == 2) or (
                abs(self.pos[0] - new[0]) == 2 and abs(self.pos[1] - new[1]) == 1)

    # returns all potential moves
    def getMoves(self, logicBoard):
        sub_moves = []
        moves = []

        sub_moves.append((self.pos[0] + 2, self.pos[1] + 1))
        sub_moves.append((self.pos[0] + 2, self.pos[1] - 1))
        sub_moves.append((self.pos[0] - 2, self.pos[1] + 1))
        sub_moves.append((self.pos[0] - 2, self.pos[1] - 1))

        sub_moves.append((self.pos[0] + 1, self.pos[1] + 2))
        sub_moves.append((self.pos[0] + 1, self.pos[1] - 2))
        sub_moves.append((self.pos[0] - 1, self.pos[1] + 2))
        sub_moves.append((self.pos[0] - 1, self.pos[1] - 2))

        for move in sub_moves:
            if -1 < move[0] < 8 and -1 < move[1] < 8:
                if logicBoard[move[0], move[1]] is None:
                    moves.append(move)
                elif logicBoard[move[0], move[1]].isWhite != self.isWhite:
                    moves.append(move)

        return moves
