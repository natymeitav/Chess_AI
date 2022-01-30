from stockfish import Stockfish
import copy


class AFO:

    def __init__(self):
        self.engine = Stockfish(path="stockfishEngine/stockfish_14.1_win_x64_avx2.exe")

    # find best next move
    def make_move(self, logic,black, white):
        move = self.engine.get_best_move()
        print(move)

        positions = self.code_to_positions(move)
        if positions is None:
            return MinMax.make_move(logic,black,white)
        else:
            return positions

    def code_to_positions(self,code):
        if code is None:
            return None
        moving = code[:2]
        target = code[2:]

        moving = [8-int(moving[1]),ord(moving[0])-ord('a')]
        target = [8-int(target[1]),ord(target[0])-ord('a')]

        return [moving,target]

    def positions_to_code(self,moving,target):
        moving = str(chr(moving[1]+ord('a'))) + str(8-moving[0])
        target = str(chr(target[1] + ord('a'))) + str(8-target[0])

        return moving + target

    def update_board(self,moving,target):
        move = self.positions_to_code(moving,target)
        print(move)
        self.engine.make_moves_from_current_position([move])

class MinMax:
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
    def make_move(logic, black, white):

        # setup max values
        max_val = float('-inf')
        max_piece = None

        # find best move for black
        for board in MinMax.getBoards(logic, white):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = MinMax.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = MinMax.getMin(board[0], temp_black, temp_white, 1) - MinMax.evaluation_val(black, white, logic)

            if MinMax.checkEndGame(black, white) != 1:
                value = MinMax.checkEndGame(black, white)

            if value > max_val:
                max_val = value
                max_piece = board[1]
        return max_piece

    @staticmethod
    def getMax(logic, black, white, depth):

        # check for max depth
        if depth == 3:
            return -1*MinMax.evaluation_val(black, white, logic)

        # setup max values
        max_val = float('-inf')

        # find best move for black
        for board in MinMax.getBoards(logic, white):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            if MinMax.checkEndGame(black, white) != 1:
                return MinMax.checkEndGame(black, white)

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                black, white = MinMax.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = MinMax.getMin(board[0], temp_black, temp_white, depth + 1) - MinMax.evaluation_val(black, white, logic)
            if value > max_val:
                max_val = value

        return max_val

    @staticmethod
    def getMin(logic, black, white, depth):

        # check for max depth
        if depth == 3:
            return -1*MinMax.evaluation_val(black, white, logic)

        # setup mon values
        min_val = float('inf')

        # find worst move for black
        for board in MinMax.getBoards(logic, black):

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            if MinMax.checkEndGame(black, white) != 1:
                return MinMax.checkEndGame(black, white)

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = MinMax.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            value = MinMax.getMax(board[0], temp_black, temp_white, depth + 1) - MinMax.evaluation_val(black, white, logic)
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

    # check for win or tie
    @staticmethod
    def checkEndGame(black,white):
        # check for white win
        endgame = 1
        if str(black[4]) != "K0":
            endgame = 9999
        # check for black win
        elif str(white[11]) != "K1":
            endgame = -9999
        # check for insufficient material
        elif len(set(white + black)) <= 3:
            endgame = 0

        return endgame

    # returns value of board
    @staticmethod
    def evaluation_val(black, white, logic):
        return 0.7 * MinMax.sum_val(black, white) + 0.3 * MinMax.space_val(black, white, logic)

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