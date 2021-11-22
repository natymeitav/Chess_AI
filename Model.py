import copy
import json
import random

import numpy as np


class CPU:
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
    def makeMove(logic, black, white):

        # setup max values
        max_val = float('-inf')
        max_piece = None

        # find best move for black
        for board in CPU.getBoards(logic, black):

            capture_val = 0

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            endgame = CPU.checkEndGame(black, white)
            if endgame != -999:
                return endgame

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white, capture_val = CPU.deletePiece(temp_black, temp_white,
                                                                      logic[piece_pos[0], piece_pos[1]],
                                                                      board[0][piece_pos[0], piece_pos[1]])

            value = CPU.getMin(board[0], temp_black, temp_white, 1) + capture_val
            if value > max_val:
                max_val = value
                max_piece = board[1]
        return max_piece

    @staticmethod
    def getMax(logic, black, white, depth):

        # check for max depth
        if depth == 2:
            return 0

        # setup max values
        max_val = float('-inf')

        # find best move for black
        for board in CPU.getBoards(logic, black):
            capture_val = 0

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(temp_white)

            endgame = CPU.checkEndGame(black, white)
            if endgame != -999:
                return endgame

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                black, white, capture_val = CPU.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]],
                                                            board[0][piece_pos[0], piece_pos[1]])

            value = CPU.getMin(board[0], temp_black, temp_white, depth + 1) + capture_val
            if value > max_val:
                max_val = value

        return max_val

    @staticmethod
    def getMin(logic, black, white, depth):

        # check for max depth
        if depth == 2:
            return 0

        # setup mon values
        min_val = float('inf')

        # find worst move for black
        for board in CPU.getBoards(logic, white):
            capture_val = 0

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            endgame = CPU.checkEndGame(black, white)
            if endgame != -999:
                return endgame

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white, capture_val = CPU.deletePiece(temp_black, temp_white,
                                                                      logic[piece_pos[0], piece_pos[1]],
                                                                      board[0][piece_pos[0], piece_pos[1]])

            value = CPU.getMax(board[0], temp_black, temp_white, depth + 1) + capture_val
            if value < min_val:
                min_val = value

        return min_val

    @staticmethod
    def deletePiece(black, white, captured, moving):
        if captured.isWhite:
            white[captured.serialNum] = None
        else:
            black[captured.serialNum] = None
        return black, white, captured.value - moving.value

    # check for win or tie
    @staticmethod
    def checkEndGame(black, white):
        # check for white win
        endgame = -999
        if str(black[4]) != "K0":
            endgame = 1
        # check for black win
        elif str(white[12]) != "K1":
            endgame = -1
        # check for insufficient material
        elif len(set(white + black)) == 3:
            endgame = 0

        return endgame

    @staticmethod
    def printBoard(listLogicBoard):
        for row in range(len(listLogicBoard)):
            print("")
            for col in range(len(listLogicBoard)):
                square = listLogicBoard[row, col]
                if square is None:
                    print("--", end=" ")
                else:
                    print(square, end=" ")
        print("")

    @staticmethod
    def printLine(line):
        for row in range(len(line)):
            square = line[row]
            if square is None:
                print("--", end=" ")
            else:
                print(square, end=" ")
        print("")


class Learner:

    # plans board's next move
    @staticmethod
    def make_move(logicBoard, pieces):
        potential_moves = Learner.getBoards(logicBoard, pieces)

        best_move = random.choice(potential_moves)
        best_value = Learner.get_past_val(Learner.boardToString(best_move[0]))

        for move in potential_moves:
            val = Learner.get_past_val(Learner.boardToString(move[0]))
            if val > best_value:
                best_value = val
                best_move = move

        return best_move[1]

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

    # get value of move from memories
    @staticmethod
    def get_past_val(move):
        memories = open("memories.json", "r+")

        data = json.load(memories)

        if move in data:
            memories.close()
            return data[move]
        else:
            memories.close()
            return 0.1

    # get capture val
    @staticmethod
    def get_capture_val(moving, target):
        if target is None:
            return 0
        return target.value - moving.value

    @staticmethod
    # learns given path
    def learn_move(move, last_val, endgame):
        move, moving, captured = move  # unpack move

        memories = open("memories.json", "r+")
        data = json.load(memories)
        value = Learner.get_past_val(move) + 0.7 * (
                    last_val - Learner.get_past_val(move) + endgame) + 0.3 * Learner.get_capture_val(moving, captured)

        if move not in data:
            print("")
            print("--new move learned--")
            print(value)

        data[move] = value

        memories.seek(0)
        memories.truncate()

        json.dump(data, memories)

    @staticmethod
    # learns current route
    def learn_route(route, endgame):
        last = endgame

        while len(route) != 0:
            move = route[len(route) - 1]

            Learner.learn_move(move, Learner.get_past_val(last), endgame)
            last = move[0]

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


class randomCPU:

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

    # returns a random move
    @staticmethod
    def make_move(logicBoard, pieces):
        potential_moves = randomCPU.getBoards(logicBoard, pieces)

        best_move = random.choice(potential_moves)
        return best_move[1]
