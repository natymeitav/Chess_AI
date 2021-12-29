import copy
import json
import random

# Learner's heuristic functions
class Evaluations:

    # return the ratio between relativistic score based on the heuristic functions
    @staticmethod
    def evaluation_val(black, white, logic):
        raw_value = 0.7*Evaluations.sum_val(black, white) + 0.3*Evaluations.space_val(black, white, logic)
        return raw_value

    # returns the difference of black's and white's space
    @staticmethod
    def space_val(black, white, logic):
        val = 0
        for piece in black:
            if piece is not None:
                val += len(piece.getMoves(logic))

        for piece in white:
            if piece is not None:
                val -= len(piece.getMoves(logic))

        return val

    # returns sum of pieces values
    @staticmethod
    def sum_val(black, white):
        sum = 0
        pieces = black + white
        for piece in pieces:
            if piece is not None:
                sum += piece.value
        return sum

class Learner:

    # plans board's next move
    @staticmethod
    def make_move(logicBoard, black, white):
        potential_moves, black, white = Learner.getBoards(logicBoard, black, white)

        best_move = random.choice(potential_moves)
        best_value = Learner.get_past_val(Learner.boardToString(best_move[0]))
        if best_value == -999:
            best_value = Evaluations.evaluation_val(black, white, best_move[0])
        for move in potential_moves:
            val = Learner.get_past_val(Learner.boardToString(move[0]))
            if val == -999:
                val = Evaluations.evaluation_val(black, white, move[0])

            if val > best_value:
                best_value = val
                best_move = move

        print(Learner.boardToString(best_move[0]))
        print("best val: "+str(best_value))
        return best_move[1]

    # return array of posible moves [board,[position before, position after]]
    @staticmethod
    def getBoards(logic, black, white):
        boards = []
        for piece in black:
            if piece is not None:
                for move in piece.getMoves(logic):
                    temp_logic = copy.deepcopy(logic)
                    temp_piece = copy.deepcopy(piece)

                    piece_pos = piece.pos

                    # check for capture
                    if temp_logic[move[0], move[1]] is not None:
                        if temp_logic[move[0], move[1]].isWhite != temp_piece.isWhite:
                            black, white = Learner.deletePiece(black,white,temp_logic[move[0], move[1]])

                    # update boards
                    temp_logic[move[0], move[1]] = temp_piece
                    temp_logic[temp_piece.pos[0], temp_piece.pos[1]] = None

                    # update piece's first move
                    if temp_logic[move[0], move[1]].firstMove:
                        temp_logic[move[0], move[1]].firstMove = False

                    # update piece's position
                    temp_logic[move[0], move[1]].pos = move

                    boards.append([temp_logic, [piece_pos, (move[0], move[1])]])

        return boards, black, white

    @staticmethod
    def deletePiece(black, white, captured):
        if captured.isWhite:
            white[captured.serialNum] = None
        else:
            black[captured.serialNum] = None
        return black, white

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
            return -999

    @staticmethod
    # learns given path
    def learn_move(move, last_val):
        memories = open("memories.json", "r+")
        data = json.load(memories)

        line, evaluation = move
        val = Learner.get_past_val(line)

        if line not in data:
            print("")
            print("--new move learned--")
            val = evaluation

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

            last = Learner.learn_move(move, last)

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
