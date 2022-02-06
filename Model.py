from kivy.clock import Clock
from stockfish import Stockfish


class AFO:

    def __init__(self, parent):
        self.engine = Stockfish(path="stockfishEngine/stockfish_14.1_win_x64_avx2.exe")
        self.parent = parent

    # find best next move
    def make_move(self, logic, black, white):
        move = self.engine.get_best_move()
        print(move)

        positions = self.code_to_positions(move)
        if positions is None:
            return self.checkEndGame(logic, black, white)
        else:
            return positions

    # check for win or tie
    def checkEndGame(self, logic, black, white):
        endgame = 0
        # check for white win
        if black[4].isThreatened(white, logic):
            endgame = -1
        # check for black win
        elif white[12].isThreatened(black, logic):
            endgame = 1

        self.parent.endgame(endgame)
        return [(0,0),(0,0)]

    def code_to_positions(self, code):
        moving = code[:2]
        target = code[2:]

        moving = [int(moving[1]), ord(moving[0]) - ord('a')]
        target = [int(target[1]), ord(target[0]) - ord('a')]

        return [moving, target]

    def positions_to_code(self, positions):
        moving, target = positions

        moving = str(chr(moving[1])) + str(chr(moving[0] + ord('a')))
        target = str(chr(target[1])) + str(chr(target[0] + ord('a')))

        return moving + target

    def update_board(self, positions):
        move = self.positions_to_code(positions)
        self.engine.make_moves_from_current_position([move])

    def code_to_positions(self, code):
        if code is None:
            return None
        moving = code[:2]
        target = code[2:]

        moving = [8 - int(moving[1]), ord(moving[0]) - ord('a')]
        target = [8 - int(target[1]), ord(target[0]) - ord('a')]

        return [moving, target]

    def positions_to_code(self, moving, target):
        moving = str(chr(moving[1] + ord('a'))) + str(8 - moving[0])
        target = str(chr(target[1] + ord('a'))) + str(8 - target[0])

        return moving + target

    def update_board(self, moving, target):
        move = self.positions_to_code(moving, target)
        print(move)
        self.engine.make_moves_from_current_position([move])
