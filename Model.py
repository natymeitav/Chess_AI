import copy
import json
import random

import numpy as np


class Rival:

    # return array of posible moves [board,[position before, position after]]
    @staticmethod
    def getBoards(logic, pieces):
        boards = []
        for piece in pieces:
            if piece is not None:
                for move in piece.getMoves(logic):
                    temp_logic = copy.deepcopy(logic)
                    temp_piece = copy.deepcopy(piece)

                    piece_pos = piece.pos

                    # update boards
                    temp_logic[move[0], move[1]] = temp_piece
                    temp_logic[temp_piece.pos[0], temp_piece.pos[1]] = None

                    # update piece's first move
                    if temp_logic[move[0], move[1]].firstMove:
                        temp_logic[move[0], move[1]].firstMove = False

                    # update piece's position
                    temp_logic[move[0], move[1]].pos = move

                    boards.append([temp_logic, [piece_pos, (move[0], move[1])]])

        return boards

    # find best next move
    @staticmethod
    def make_move(logic, white):
        boards = Rival.getBoards(logic, white)

        options = Rival.get_options(boards)

        if not options:
            options = boards

        choice = random.choice(options)
        return choice[1], Rival.boardToString(choice[0])

    @staticmethod
    def get_options(boards):
        options = []
        memories = open("memories1.json", "r+")

        for board in boards:
            if Rival.boardToString(board[0]) not in memories:
                options.append(board)

        return options

    @staticmethod
    # learns given path
    def learn_move(move, last_val):
        memories = open("memories1.json", "r+")
        data = json.load(memories)

        line = move
        val = 0.1

        if line not in data:
            print("")
            print("--new move learned--")

        value = val + 0.7 * (last_val - val)
        print(value)

        data[line] = value

        memories.seek(0)
        memories.truncate()

        json.dump(data, memories)

        return value

    @staticmethod
    # learns current route
    def learn_route(route, endgame):
        last = endgame * 999

        while len(route) != 0:
            move = route[len(route) - 1]

            last = Rival.learn_move(move, last)

            route.pop(len(route) - 1)

    # returns the board in string form
    @staticmethod
    def boardToString(logic):
        flat = logic.flatten()
        result = ""
        last = str(flat[0])
        times = 0

        for cell in flat:
            if str(cell) == last:
                times += 1
            else:
                if times != 1:
                    result += last + str(times)
                else:
                    result += last
                last = str(cell)
                times = 1

        return result
