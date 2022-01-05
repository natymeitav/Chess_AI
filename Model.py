import copy


# bot's heuristic functions
class Evaluations:
    # returns value of board
    @staticmethod
    def evaluation_val(black, white, logic):
        return 0.7 * L_MinMax.sum_val(black, white) + 0.3 * L_MinMax.space_val(black, white, logic)

    # returns the difference of black's and white's space
    @staticmethod
    def space_val(black, white, logic):
        black_sum = 0
        for piece in black:
            if piece is not None:
                black_sum += len(piece.getMoves(logic))

        white_sum = 0
        for piece in white:
            if piece is not None:
                white_sum += len(piece.getMoves(logic))

        return black_sum - white_sum

    # returns sum of pieces values
    @staticmethod
    def sum_val(black, white):
        sum = 0
        pieces = black + white
        for piece in pieces:
            if piece is not None:
                sum += piece.value
        return sum

# learns and recalls moves
class RBD:
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

    # learn path
    @staticmethod
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


# calculates next Moves
class MinMax:

    @staticmethod
    def getMax(logic, black, white, depth):

        # check for max depth
        if depth == 0:
            return L_MinMax.evaluation_val(black, white, logic)

        # setup max values
        max_val = float('-inf')

        # find best move for black
        for board in L_MinMax.getBoards(logic, black):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            if L_MinMax.checkTie(temp_black, temp_white):
                print("tie")
                return 0

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = L_MinMax.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = L_MinMax.getMin(board[0], temp_black, temp_white, depth - 1) + Evaluations.evaluation_val(black, white, logic)
            if value > max_val:
                max_val = value

        return max_val

    @staticmethod
    def getMin(logic, black, white, depth):

        # check for max depth
        if depth == 0:
            return L_MinMax.evaluation_val(black, white, logic)

        # setup mon values
        min_val = float('inf')

        # find worst move for black
        for board in L_MinMax.getBoards(logic, white):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            if L_MinMax.checkTie(temp_black, temp_white):
                print("tie")
                return 0

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = L_MinMax.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = L_MinMax.getMax(board[0], temp_black, temp_white, depth - 1) + Evaluations.evaluation_val(black, white, logic)
            if value < min_val:
                min_val = value

        return min_val

    @staticmethod
    def deletePiece(black, white, captured):
        if captured.isWhite:
            white[captured.serialNum] = None
        else:
            black[captured.serialNum] = None
        return black, white

    # check for tie
    @staticmethod
    def checkTie(black, white):
        return len(set(white + black)) == 3

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
