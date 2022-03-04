import copy


class CPU:

    def __init__(self, pieces_im, space_im, capture_im, center_im, safety_im):
        self.pieces_im = pieces_im
        self.space_im = space_im
        self.capture_im = capture_im
        self.center_im = center_im
        self.saftey_im = safety_im


    # return array of posible moves [board,[position before, position after]]
    def getBoards(self, logic, pieces):
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
    def make_move(self, logic, black, white, depth):

        # setup values
        alpha = float('-inf')
        beta = float('inf')
        boards = CPU.getBoards(logic, black)
        max_board = boards[0][1]
        max_val = float('-inf')

        boards = CPU.ordering(CPU.getBoards(logic, black), black, white, logic,False)

        # find best move for black
        for board in boards:
            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = CPU.deletePiece(temp_black, temp_white,
                                                         logic[piece_pos[0], piece_pos[1]])

            if CPU.checkEndGame(temp_black, temp_white):
                value = CPU.checkEndGame(temp_black, temp_white)
            else:
                value = CPU.getMin(board[0], black, white, depth, alpha, beta)

            if value > max_val:
                max_val = value
                max_board = board

                if alpha < max_val:
                    alpha = max_val
                    if beta <= alpha:
                        break

        print("-----------------------------------------------------------------")
        print(str(max_board[1][1]) + " " + str(max_val))
        return max_board[1]

    @staticmethod
    def getMin(logic, black, white, depth, alpha, beta):

        # check for max depth
        if depth == 0:
            CPU.printBoard(logic)
            print("VAL: " + str(CPU.evaluation_val(black, white, logic)), end=" ")
            return CPU.evaluation_val(black, white, logic)

        # setup mon values
        min_val = float('inf')

        boards = CPU.ordering(CPU.getBoards(logic, white), white, black, logic, False)

        # find worst move for black
        for board in boards:

            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            piece_pos = board[1][1]
            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = CPU.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            if CPU.checkEndGame(temp_black, temp_white):
                return CPU.checkEndGame(temp_black, temp_white)

            value = CPU.getMax(board[0], temp_black, temp_white, depth - 1, alpha, beta)
            print(piece_pos)

            if value < min_val:
                min_val = value
                if beta > min_val:
                    beta = min_val
                    if beta <= alpha:
                        break

        print("MIN: " + str(min_val))
        return min_val

    @staticmethod
    def getMax(logic, black, white, depth, alpha, beta):

        # check for max depth
        if depth == 0:
            CPU.printBoard(logic)
            print("VAL: "+str(CPU.evaluation_val(black, white, logic)),end = " ")
            return CPU.evaluation_val(black, white, logic)

        # setup max values
        max_val = float('-inf')

        boards = CPU.ordering(CPU.getBoards(logic, black), black, white, logic,False)

        # find best move for black
        for board in boards:
            # copy black and white pieces
            temp_black = copy.deepcopy(black)
            temp_white = copy.deepcopy(white)

            piece_pos = board[1][1]

            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                temp_black, temp_white = CPU.deletePiece(temp_black, temp_white, logic[piece_pos[0], piece_pos[1]])

            if CPU.checkEndGame(temp_black, temp_white):
                return CPU.checkEndGame(temp_black, temp_white)

            value = CPU.getMin(board[0], temp_black, temp_white, depth - 1, alpha, beta)
            print(piece_pos)

            if value > max_val:
                max_val = value
                if alpha < max_val:
                    alpha = max_val
                    if beta <= alpha:
                        break

        print("MAX: " + str(max_val))
        return max_val

    @staticmethod
    def deletePiece(black, white, captured):
        if captured.isWhite:
            white[captured.serialNum] = None
        else:
            black[captured.serialNum] = None
        return black, white

    @staticmethod
    def ordering(boards, allys, enemies, logic, isWhite):
        order = []
        if isWhite:
            black = copy.deepcopy(enemies)
            white = copy.deepcopy(allys)
        else:
            black = copy.deepcopy(allys)
            white = copy.deepcopy(enemies)

        for board in boards:
            index = -1

            piece_pos = board[1][1]
            # check for capture
            if logic[piece_pos[0], piece_pos[1]] is not None:
                black, white = CPU.deletePiece(black, white,
                                               logic[piece_pos[0], piece_pos[1]])
                index = 0

            # check for dangerous position
            for enemy in white:
                if enemy is not None:
                    if piece_pos in enemy.getMoves(board[0]):
                        if len(order) - 1 > index:
                            index += 1

            # check for protection
            for ally in black:
                if ally is not None:
                    if piece_pos in ally.getMoves(board[0]):
                        if 1 < index:
                            index -= 2
                        elif index == 1:
                            index = 0

            order.insert(index, board)

        return order

    # returns value of board
    @staticmethod
    def evaluation_val(black, white, logic):
        value_sum, space_sum, center_val = CPU.sum_val(black, white, logic)
        saftey_val = CPU.safety_val(black,white,logic)
        return 0.7 * value_sum + 0.1 * space_sum + 0.2 * center_val - 0.6*saftey_val

    # returns evaluation values
    @staticmethod
    def sum_val(black, white, logic):
        sum = 0
        moves_sum = 0
        center_val = 0
        for piece in black:
            if piece is not None:
                sum += piece.value

                moves = piece.getMoves(logic)
                moves_sum += len(moves)

                # check center_control
                center_val += CPU.center_val(piece.pos,piece.value)

        for piece in white:
            if piece is not None:
                sum += piece.value

                moves = piece.getMoves(logic)
                moves_sum -= len(moves)

                # check center_control
                center_val -= CPU.center_val(piece.pos,piece.value)

        return sum, moves_sum, center_val

    # checks for control over the center
    @staticmethod
    def center_val(pos,val):
        if 3 <= pos[0] <= 4 and 3 <= pos[0] <= 4:
            return val
        elif (pos[0] == 2 or pos[0] == 5) and (pos[1] == 2 or pos[0] == 5):
            return val/2
        else:
            return 0

    @staticmethod
    def safety_val(black,white,logic):
        return len(black[4].getMoves(logic)) - len(white[12].getMoves(logic))


    # check for endgame
    @staticmethod
    def checkEndGame(black, white):
        # check for white win
        if str(black[4]) != "K0":
            return float('-inf')
        # check for black win
        elif str(white[12]) != "K1":
            return float('inf')
        # check for insufficient material
        elif len(set(white + black)) == 4:
            return 0

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
