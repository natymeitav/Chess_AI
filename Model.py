import copy

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
    def make_move(logic, black, white):

        # setup values
        alpha = float('-inf')
        beta = float('inf')
        boards = CPU.getBoards(logic, black)
        max_board = boards[0][1]
        max_val = float('-inf')

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
                value = CPU.getMin(board[0], black, white, 2, alpha, beta)

            if value > max_val:
                max_val = value
                max_board = board

                if alpha < max_val:
                    alpha = max_val
                    if beta <= alpha:
                        break

        print(str(max_board[1][1])+" "+str(max_val))
        return max_board[1]

    @staticmethod
    def getMax(logic, black, white, depth, alpha, beta):

        # check for max depth
        if depth == 0:
            return CPU.evaluation_val(black, white, logic)

        # setup max values
        max_val = float('-inf')

        # find best move for black
        for board in CPU.getBoards(logic, black):
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

            if value > max_val:
                max_val = value
                if alpha < max_val:
                    alpha = max_val
                    if beta <= alpha:
                        break

        return max_val

    @staticmethod
    def getMin(logic, black, white, depth, alpha, beta):

        # check for max depth
        if depth == 0:
            return CPU.evaluation_val(black,white,logic)

        # setup mon values
        min_val = float('inf')

        # find worst move for black
        for board in CPU.getBoards(logic, white):

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

            if value < min_val:
                min_val = value
                if beta > min_val:
                    beta = min_val
                    if beta <= alpha:
                        break

        return min_val

    @staticmethod
    def deletePiece(black, white, captured):
        if captured.isWhite:
            white[captured.serialNum] = None
        else:
            black[captured.serialNum] = None
        return black, white

    # returns value of board
    @staticmethod
    def evaluation_val(black,white,logic):
        return 0.7*CPU.sum_val(black,white,logic)+0.3*CPU.space_val(black,white,logic)

    # returns the difference of black's and white's space
    @staticmethod
    def space_val(black,white,logic):
        black_sum = 0
        for piece in black:
            if piece is not None:
                black_sum += len(piece.getMoves(logic))

        white_sum = 0
        for piece in white:
            if piece is not None:
                white_sum += len(piece.getMoves(logic))

        return black_sum - white_sum

    # counts the number of pieces that protect pos
    @staticmethod
    def protection_val(allys,pos,logic):
        count = 0
        for piece in allys:
            if piece is not None:
                if pos in piece.getMoves(logic):
                    count += 1
        return count

    # returns sum of pieces values
    @staticmethod
    def sum_val(black,white,logic):
        sum = 0
        for piece in black:
            if piece is not None:
                sum += piece.value*CPU.protection_val(black,piece.pos,logic)

        for piece in white:
            if piece is not None:
                sum += piece.value*CPU.protection_val(white,piece.pos,logic)
        return sum

    # check for endgame
    @staticmethod
    def checkEndGame(black, white):
        # check for white win
        if str(black[4]) != "K0":
            return -999
        # check for black win
        elif str(white[12]) != "K1":
            return 999
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
