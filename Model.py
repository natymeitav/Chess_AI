from stockfish import Stockfish
import random


class AFO:

    def __init__(self):
        self.engine = Stockfish(path="stockfishEngine/stockfish_14.1_win_x64_avx2.exe")
    # find best next move
    def make_move(self, logic, white):
        move = self.engine.get_best_move()

        return self.code_to_positions(move)

    def code_to_positions(self,code):
        moving = code[:2]
        target = code[2:]

        moving = [int(moving[1]),ord(moving[0])-ord('a')]
        target = [int(target[1]),ord(target[0])-ord('a')]

        return [moving,target]

    def positions_to_code(self,positions):
        moving, target = positions

        moving = str(chr(moving[1])) + str(chr(moving[0]+ord('a')))
        target = str(chr(target[1])) + str(chr(target[0] + ord('a')))

        return moving + target

    def update_board(self,positions):
        move = self.positions_to_code(positions)
        self.engine.make_moves_from_current_position([move])
